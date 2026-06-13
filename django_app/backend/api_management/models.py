import secrets
import bcrypt
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class APIClient(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_client')
    company_name = models.CharField(max_length=255)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.plan})"


class APIKey(models.Model):
    client = models.ForeignKey(APIClient, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=64, unique=True)
    hashed_secret = models.CharField(max_length=128)
    name = models.CharField(max_length=100, default='Default Key')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    @staticmethod
    def hash_secret(plain_secret):
        return bcrypt.hashpw(
            plain_secret.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def verify_secret(self, plain_secret):
        return bcrypt.checkpw(
            plain_secret.encode('utf-8'),
            self.hashed_secret.encode('utf-8')
        )

    def is_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False

    def __str__(self):
        return f"{self.client.company_name} - {self.name}"


class RateLimit(models.Model):
    TIER_LIMITS = {
        'free':       {'minute': 10,  'hour': 100,    'day': 500},
        'basic':      {'minute': 10,  'hour': 100,    'day': 500},
        'premium':    {'minute': 60,  'hour': 1000,   'day': 10000},
        'enterprise': {'minute': 300, 'hour': 10000,  'day': 100000},
    }

    client = models.OneToOneField(APIClient, on_delete=models.CASCADE, related_name='rate_limit')
    requests_per_minute = models.IntegerField(default=10)
    requests_per_hour = models.IntegerField(default=100)
    requests_per_day = models.IntegerField(default=500)

    @classmethod
    def create_for_client(cls, client):
        limits = cls.TIER_LIMITS.get(client.plan, cls.TIER_LIMITS['free'])
        return cls.objects.create(
            client=client,
            requests_per_minute=limits['minute'],
            requests_per_hour=limits['hour'],
            requests_per_day=limits['day'],
        )

    def __str__(self):
        return f"{self.client.company_name} - Rate Limit"


class APIRequestLog(models.Model):
    client = models.ForeignKey(APIClient, on_delete=models.CASCADE, related_name='request_logs', null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.endpoint} - {self.status_code} - {self.timestamp}"


class Webhook(models.Model):
    EVENT_CHOICES = [
        ('price_alert', 'Price Alert'),
        ('portfolio_update', 'Portfolio Update'),
        ('risk_alert', 'Risk Alert'),
        ('market_open', 'Market Open'),
        ('market_close', 'Market Close'),
        ('score_updated', 'Score Updated'),
        ('anomaly_flagged', 'Anomaly Flagged'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('failed', 'Failed'),
    ]

    client = models.ForeignKey(APIClient, on_delete=models.CASCADE, related_name='webhooks')
    url = models.URLField()
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    secret = models.CharField(max_length=64)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    failure_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.company_name} - {self.event_type}"


class WebhookDelivery(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='deliveries')
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_code = models.IntegerField(null=True, blank=True)
    delivered_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.webhook} - {self.status}"
