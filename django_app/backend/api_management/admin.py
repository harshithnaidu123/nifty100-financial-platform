from django.contrib import admin

from .models import (APIClient, APIKey, APIRequestLog, RateLimit, Webhook,
                     WebhookDelivery)


@admin.register(APIClient)
class APIClientAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'plan', 'is_active', 'created_at']
    list_filter = ['plan', 'is_active']
    search_fields = ['company_name', 'user__username', 'user__email']


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['client', 'name', 'is_active', 'created_at', 'last_used', 'expires_at']
    list_filter = ['is_active']
    search_fields = ['client__company_name', 'name']
    readonly_fields = ['key', 'hashed_secret', 'created_at', 'last_used']


@admin.register(RateLimit)
class RateLimitAdmin(admin.ModelAdmin):
    list_display = ['client', 'requests_per_minute', 'requests_per_hour', 'requests_per_day']
    search_fields = ['client__company_name']


@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'method', 'status_code', 'client', 'ip_address', 'timestamp', 'response_time_ms']
    list_filter = ['method', 'status_code']
    search_fields = ['endpoint', 'client__company_name']
    readonly_fields = ['timestamp']


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['client', 'event_type', 'url', 'status', 'created_at', 'last_triggered', 'failure_count']
    list_filter = ['event_type', 'status']
    search_fields = ['client__company_name', 'url']
    readonly_fields = ['secret', 'created_at']


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    list_display = ['webhook', 'status', 'response_code', 'delivered_at']
    list_filter = ['status']
    readonly_fields = ['delivered_at']
