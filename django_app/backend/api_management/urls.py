from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_client, name='api-register'),
    path('status/', views.get_api_status, name='api-status'),
    path('partner/', views.channel_partner_data, name='channel-partner'),
    path('webhooks/', views.list_webhooks, name='list-webhooks'),
    path('webhooks/create/', views.create_webhook, name='create-webhook'),
    path('keys/rotate/', views.rotate_api_key, name='rotate-key'),
    path('logs/', views.request_logs, name='request-logs'),
]
