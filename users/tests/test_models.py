import pytest
from allauth.account.models import EmailAddress
from allauth.account.utils import sync_user_email_addresses
from django.contrib.auth import get_user_model
from django.db import IntegrityError

USER = get_user_model()


@pytest.mark.django_db
class TestUser:
    @pytest.fixture
    def user(self):
        return USER.objects.create(
            first_name="Test", last_name="Name", email="test@example.com"
        )

    @pytest.fixture
    def verified_email_address(self, user):
        return EmailAddress.objects.create(
            user=user, verified=True, email="test@example.com"
        )

    @pytest.fixture
    def unverified_email_address(self, user):
        return EmailAddress.objects.create(
            user=user, verified=False, email="test@example.com"
        )

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = USER.objects.create_user(
            email=email,
            password=password,
        )
        assert user.email == email
        assert user.check_password(password)

    def test_new_user_without_email_raises_error(self):
        with pytest.raises(ValueError):
            USER.objects.create_user('', 'test123')

    def test_create_superuser(self):
        user = USER.objects.create_superuser('test@example.com', 'test123')
        assert user.is_superuser
        assert user.is_staff

    def test_new_user_email_normalized(self):
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected_email in sample_email:
            user = USER.objects.create_user(email=email, password='test123')
            assert user.email == expected_email
            USER.objects.all().delete()

    def test_has_verified_email_verified(self, user):
        assert not EmailAddress.objects.filter(user=user).exists()
        assert not user.has_verified_email
        email = EmailAddress.objects.create(
            user=user, verified=False, email="test@example.com"
        )
        addresses = EmailAddress.objects.filter(user=user)
        assert addresses.exists()
        assert addresses.count() == 1
        assert not user.has_verified_email
        email.verified = True
        email.save()
        assert user.has_verified_email

    def test_has_verified_email_current_email_different_to_verified(
            self, user, verified_email_address
    ):
        verified_email_address.email = "test2@example.com"
        verified_email_address.save()
        addresses = EmailAddress.objects.filter(user=user)
        assert addresses.exists()
        assert addresses.count() == 1
        assert not user.has_verified_email

    def test_case_insensitive_email(self, user):
        with pytest.raises(IntegrityError):
            USER.objects.create(email="TEST@example.com")

    def test_save_changing_email(self, user, unverified_email_address):
        addresses = EmailAddress.objects.filter(user=user)
        assert addresses.exists()
        assert addresses.count() == 1
        assert not user.has_verified_email
        user.email = "test2@example.com"
        user.save()
        sync_user_email_addresses(user)
        addresses = EmailAddress.objects.filter(user=user)
        assert addresses.count() == 2
        assert user.email == "test2@example.com"

    def test_save_not_changing_email(self, user, unverified_email_address):
        addresses = EmailAddress.objects.filter(user=user)
        assert addresses.exists()
        assert addresses.count() == 1
        assert not user.has_verified_email
        user.first_name = "George"
        user.save()
        assert EmailAddress.objects.filter(user=user).count() == 1
        assert user.email == "test@example.com"
        assert user.first_name == "George"
