import secrets

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api_management.models import APIClient, APIKey, RateLimit


class Command(BaseCommand):
    help = "Create a test channel partner with API key for development and testing"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, default="test_partner")
        parser.add_argument("--company", type=str, default="Test Partner Company")
        parser.add_argument(
            "--plan",
            type=str,
            default="premium",
            choices=["free", "basic", "premium", "enterprise"],
        )

    def handle(self, *args, **options):
        username = options["username"]
        company = options["company"]
        plan = options["plan"]

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("User already exists. Recreating..."))
            User.objects.filter(username=username).delete()

        user = User.objects.create_user(
            username=username,
            email=username + "@testpartner.com",
            password=secrets.token_hex(16),
        )

        client = APIClient.objects.create(
            user=user,
            company_name=company,
            plan=plan,
            is_active=True,
        )

        RateLimit.create_for_client(client)

        plain_secret = secrets.token_hex(32)
        hashed = APIKey.hash_secret(plain_secret)
        api_key = APIKey(client=client, name="Test Primary Key", hashed_secret=hashed)
        api_key.save()

        self.stdout.write(self.style.SUCCESS("========================================"))
        self.stdout.write(self.style.SUCCESS("  Test Partner Created Successfully"))
        self.stdout.write(self.style.SUCCESS("========================================"))
        self.stdout.write("  Company   : " + company)
        self.stdout.write("  Username  : " + username)
        self.stdout.write("  Plan      : " + plan)
        self.stdout.write("  API Key   : " + api_key.key)
        self.stdout.write("  API Secret: " + plain_secret)
        self.stdout.write(self.style.WARNING("  IMPORTANT: Save the API Secret now."))
        self.stdout.write(self.style.WARNING("  It is bcrypt-hashed and cannot be recovered."))
        self.stdout.write(self.style.SUCCESS("========================================"))
