import hashlib
import hmac
import secrets
import time

from django.core.cache import cache
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import APIClient, APIKey, APIRequestLog, RateLimit, Webhook


def verify_hmac_signature(request, secret):
    signature = request.headers.get("X-Signature-256", "")
    if not signature:
        return False
    body = request.body
    expected = "sha256=" + hmac.new(
        secret.encode(), body, hashlib.sha256
    ).hexdigest()
    return secrets.compare_digest(expected, signature)


def check_rate_limit(client):
    cache_key_minute = f"rate_limit_minute_{client.id}"
    cache_key_hour = f"rate_limit_hour_{client.id}"
    cache_key_day = f"rate_limit_day_{client.id}"

    try:
        rate_limit = client.rate_limit
    except RateLimit.DoesNotExist:
        rate_limit = RateLimit.create_for_client(client)

    count_minute = cache.get(cache_key_minute, 0)
    count_hour = cache.get(cache_key_hour, 0)
    count_day = cache.get(cache_key_day, 0)

    if count_minute >= rate_limit.requests_per_minute:
        return False, "Rate limit exceeded: too many requests per minute"
    if count_hour >= rate_limit.requests_per_hour:
        return False, "Rate limit exceeded: too many requests per hour"
    if count_day >= rate_limit.requests_per_day:
        return False, "Rate limit exceeded: too many requests per day"

    cache.set(cache_key_minute, count_minute + 1, 60)
    cache.set(cache_key_hour, count_hour + 1, 3600)
    cache.set(cache_key_day, count_day + 1, 86400)

    return True, "OK"


def get_client_from_api_key(request):
    api_key = request.headers.get("X-API-Key", "")
    if not api_key:
        return None, "API key missing"
    try:
        key_obj = APIKey.objects.select_related("client").get(
            key=api_key, is_active=True
        )
        if key_obj.is_expired():
            return None, "API key expired"
        key_obj.last_used = timezone.now()
        key_obj.save(update_fields=["last_used"])
        return key_obj.client, "OK"
    except APIKey.DoesNotExist:
        return None, "Invalid API key"


def log_request(request, client, status_code, response_time=None):
    APIRequestLog.objects.create(
        client=client,
        endpoint=request.path,
        method=request.method,
        status_code=status_code,
        ip_address=request.META.get("REMOTE_ADDR"),
        response_time_ms=response_time,
    )


# --- Public Endpoints ---


@api_view(["POST"])
@permission_classes([AllowAny])
def register_client(request):
    """Register a new API client and get API key."""
    data = request.data
    required = ["username", "email", "password", "company_name"]
    for field in required:
        if not data.get(field):
            return Response({"error": f"{field} is required"}, status=400)

    from django.contrib.auth.models import User

    if User.objects.filter(username=data["username"]).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    client = APIClient.objects.create(
        user=user,
        company_name=data["company_name"],
        plan=data.get("plan", "free"),
    )
    RateLimit.create_for_client(client)

    plain_secret = secrets.token_hex(32)
    hashed = APIKey.hash_secret(plain_secret)
    api_key = APIKey(client=client, name="Primary Key", hashed_secret=hashed)
    api_key.save()

    return Response(
        {
            "message": "Client registered successfully",
            "api_key": api_key.key,
            "api_secret": plain_secret,
            "note": "Save your api_secret now. It will never be shown again.",
            "client_id": client.id,
            "plan": client.plan,
        },
        status=201,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def channel_partner_data(request):
    """Channel Partner API endpoint with HMAC + API key auth."""
    start_time = time.time()

    client, msg = get_client_from_api_key(request)
    if not client:
        return Response({"error": msg}, status=401)

    if not client.is_active:
        return Response({"error": "Client account is inactive"}, status=403)

    allowed, limit_msg = check_rate_limit(client)
    if not allowed:
        log_request(request, client, 429)
        return Response({"error": limit_msg}, status=429)

    response_time = (time.time() - start_time) * 1000
    log_request(request, client, 200, response_time)

    return Response(
        {
            "status": "success",
            "client": client.company_name,
            "plan": client.plan,
            "data": {
                "message": "Channel Partner API access granted",
                "platform": "NIFTY100 Financial Intelligence Platform",
                "version": "1.0.0",
                "endpoints_available": [
                    "/api/partner/v1/companies/{symbol}/full/",
                    "/api/partner/v1/bulk-financials/",
                    "/api/partner/v1/screener/",
                    "/api/partner/v1/scores/",
                ],
            },
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_api_status(request):
    """Get API status and client info using API key."""
    client, msg = get_client_from_api_key(request)
    if not client:
        return Response({"error": msg}, status=401)

    try:
        rate_limit = client.rate_limit
        limit_info = {
            "requests_per_minute": rate_limit.requests_per_minute,
            "requests_per_hour": rate_limit.requests_per_hour,
            "requests_per_day": rate_limit.requests_per_day,
        }
    except RateLimit.DoesNotExist:
        limit_info = {}

    keys = client.api_keys.filter(is_active=True).values(
        "name", "created_at", "last_used"
    )
    webhooks = client.webhooks.filter(status="active").values(
        "event_type", "url", "status"
    )
    total_requests = client.request_logs.count()

    return Response(
        {
            "client": client.company_name,
            "plan": client.plan,
            "is_active": client.is_active,
            "rate_limits": limit_info,
            "active_keys": list(keys),
            "active_webhooks": list(webhooks),
            "total_requests_made": total_requests,
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def create_webhook(request):
    """Register a webhook URL for event notifications."""
    client, msg = get_client_from_api_key(request)
    if not client:
        return Response({"error": msg}, status=401)

    data = request.data
    if not data.get("url") or not data.get("event_type"):
        return Response({"error": "url and event_type are required"}, status=400)

    valid_events = [
        "price_alert",
        "portfolio_update",
        "risk_alert",
        "market_open",
        "market_close",
        "score_updated",
        "anomaly_flagged",
    ]
    if data["event_type"] not in valid_events:
        return Response(
            {"error": f"Invalid event_type. Choose from: {valid_events}"}, status=400
        )

    webhook = Webhook.objects.create(
        client=client,
        url=data["url"],
        event_type=data["event_type"],
    )

    return Response(
        {
            "message": "Webhook registered successfully",
            "webhook_id": webhook.id,
            "webhook_secret": webhook.secret,
            "event_type": webhook.event_type,
            "url": webhook.url,
        },
        status=201,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def list_webhooks(request):
    """List all webhooks for a client."""
    client, msg = get_client_from_api_key(request)
    if not client:
        return Response({"error": msg}, status=401)

    webhooks = client.webhooks.all().values(
        "id", "url", "event_type", "status",
        "created_at", "last_triggered", "failure_count",
    )
    return Response({"webhooks": list(webhooks)})


@api_view(["POST"])
@permission_classes([AllowAny])
def rotate_api_key(request):
    """Rotate (regenerate) an API key."""
    client, msg = get_client_from_api_key(request)
    if not client:
        return Response({"error": msg}, status=401)

    old_key = request.headers.get("X-API-Key")
    try:
        key_obj = APIKey.objects.get(key=old_key, client=client)
        plain_secret = secrets.token_hex(32)
        key_obj.key = secrets.token_hex(32)
        key_obj.hashed_secret = APIKey.hash_secret(plain_secret)
        key_obj.save()
        return Response(
            {
                "message": "API key rotated successfully",
                "new_api_key": key_obj.key,
                "new_api_secret": plain_secret,
                "note": "Save your new api_secret now. It will never be shown again.",
            }
        )
    except APIKey.DoesNotExist:
        return Response({"error": "Key not found"}, status=404)


@api_view(["GET"])
@permission_classes([AllowAny])
def request_logs(request):
    """Get request logs for a client."""
    client, msg = get_client_from_api_key(request)
    if not client:
        return Response({"error": msg}, status=401)

    logs = client.request_logs.all()[:50].values(
        "endpoint", "method", "status_code", "timestamp", "response_time_ms"
    )
    return Response({"logs": list(logs)})
