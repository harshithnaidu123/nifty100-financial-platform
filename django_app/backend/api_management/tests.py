from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import APIClient, APIKey, RateLimit, Webhook


class TestAPIClientModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.client_obj = APIClient.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )

    def test_api_client_created(self):
        self.assertEqual(self.client_obj.company_name, 'Test Company')
        self.assertEqual(self.client_obj.plan, 'basic')
        self.assertTrue(self.client_obj.is_active)

    def test_api_client_str(self):
        self.assertEqual(str(self.client_obj), 'Test Company (basic)')


class TestAPIKeyModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='test2@test.com',
            password='testpass123'
        )
        self.client_obj = APIClient.objects.create(
            user=self.user,
            company_name='Test Company 2',
            plan='free'
        )
        self.api_key = APIKey.objects.create(
            client=self.client_obj,
            name='Test Key',
            hashed_secret=APIKey.hash_secret('testsecret123')
        )

    def test_api_key_generated(self):
        self.assertIsNotNone(self.api_key.key)
        self.assertEqual(len(self.api_key.key), 64)

    def test_api_secret_generated(self):
        self.assertIsNotNone(self.api_key.hashed_secret)
        self.assertGreater(len(self.api_key.hashed_secret), 0)

    def test_api_key_not_expired(self):
        self.assertFalse(self.api_key.is_expired())

    def test_api_key_str(self):
        self.assertEqual(str(self.api_key), 'Test Company 2 - Test Key')


class TestRateLimitModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser3',
            email='test3@test.com',
            password='testpass123'
        )
        self.client_obj = APIClient.objects.create(
            user=self.user,
            company_name='Test Company 3',
            plan='premium'
        )
        self.rate_limit = RateLimit.objects.create(
            client=self.client_obj,
            requests_per_minute=60,
            requests_per_hour=1000,
            requests_per_day=10000
        )

    def test_rate_limit_defaults(self):
        self.assertEqual(self.rate_limit.requests_per_minute, 60)
        self.assertEqual(self.rate_limit.requests_per_hour, 1000)
        self.assertEqual(self.rate_limit.requests_per_day, 10000)

    def test_rate_limit_str(self):
        self.assertEqual(str(self.rate_limit), 'Test Company 3 - Rate Limit')


class TestWebhookModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser4',
            email='test4@test.com',
            password='testpass123'
        )
        self.client_obj = APIClient.objects.create(
            user=self.user,
            company_name='Test Company 4',
            plan='enterprise'
        )
        self.webhook = Webhook.objects.create(
            client=self.client_obj,
            url='https://example.com/webhook',
            event_type='price_alert'
        )

    def test_webhook_created(self):
        self.assertEqual(self.webhook.event_type, 'price_alert')
        self.assertEqual(self.webhook.status, 'active')

    def test_webhook_secret_generated(self):
        self.assertIsNotNone(self.webhook.secret)
        self.assertEqual(len(self.webhook.secret), 64)

    def test_webhook_str(self):
        self.assertEqual(str(self.webhook), 'Test Company 4 - price_alert')


class TestRegisterClientAPI(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        response = self.client.post(
            '/api/v1/register/',
            data={
                'username': 'newuser',
                'email': 'new@test.com',
                'password': 'pass123',
                'company_name': 'New Company'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('api_key', data)
        self.assertIn('api_secret', data)

    def test_register_missing_fields(self):
        response = self.client.post(
            '/api/v1/register/',
            data={'username': 'onlyuser'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='dupeuser', password='pass123')
        response = self.client.post(
            '/api/v1/register/',
            data={
                'username': 'dupeuser',
                'email': 'dupe@test.com',
                'password': 'pass123',
                'company_name': 'Dupe Company'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class TestAPIStatusEndpoint(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='statususer',
            email='status@test.com',
            password='pass123'
        )
        self.client_obj = APIClient.objects.create(
            user=self.user,
            company_name='Status Company',
            plan='basic'
        )
        RateLimit.objects.create(client=self.client_obj)
        self.api_key = APIKey.objects.create(
            client=self.client_obj,
            name='Status Key',
            hashed_secret=APIKey.hash_secret('testsecret123')
        )

    def test_status_with_valid_key(self):
        response = self.client.get(
            '/api/v1/status/',
            HTTP_X_API_KEY=self.api_key.key
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['client'], 'Status Company')

    def test_status_without_key(self):
        response = self.client.get('/api/v1/status/')
        self.assertEqual(response.status_code, 401)

    def test_status_with_invalid_key(self):
        response = self.client.get(
            '/api/v1/status/',
            HTTP_X_API_KEY='invalidkey123'
        )
        self.assertEqual(response.status_code, 401)


class TestWebhookAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='webhookuser',
            email='webhook@test.com',
            password='pass123'
        )
        self.client_obj = APIClient.objects.create(
            user=self.user,
            company_name='Webhook Company',
            plan='basic'
        )
        self.api_key = APIKey.objects.create(
            client=self.client_obj,
            name='Webhook Key',
            hashed_secret=APIKey.hash_secret('testsecret123')
        )

    def test_create_webhook_success(self):
        response = self.client.post(
            '/api/v1/webhooks/create/',
            data={
                'url': 'https://example.com/hook',
                'event_type': 'price_alert'
            },
            content_type='application/json',
            HTTP_X_API_KEY=self.api_key.key
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('webhook_secret', data)

    def test_create_webhook_invalid_event(self):
        response = self.client.post(
            '/api/v1/webhooks/create/',
            data={
                'url': 'https://example.com/hook',
                'event_type': 'invalid_event'
            },
            content_type='application/json',
            HTTP_X_API_KEY=self.api_key.key
        )
        self.assertEqual(response.status_code, 400)

    def test_list_webhooks(self):
        response = self.client.get(
            '/api/v1/webhooks/',
            HTTP_X_API_KEY=self.api_key.key
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('webhooks', response.json())
