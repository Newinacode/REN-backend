from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models.OTP import OTP
from .models.user import CustomUser


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AccountApiTests(APITestCase):
    def test_register_login_and_verify_otp(self):
        register = self.client.post(
            "/auth/register/",
            {
                "email": "new@example.com",
                "mobile_number": "9811111111",
                "name": "New User",
                "password": "secret123",
            },
            format="json",
        )
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        user_id = register.data["user"]["id"]
        self.assertFalse(register.data["user"]["is_verified"])

        login = self.client.post(
            "/auth/login/",
            {"email": "new@example.com", "password": "secret123"},
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", login.data)

        otp_response = self.client.get(f"/auth/sendotp/{user_id}/")
        self.assertEqual(otp_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

        otp = OTP.objects.get(user_id=user_id)
        verify = self.client.post(
            f"/auth/verifyotp/{user_id}/",
            {"otp": otp.otp_number},
            format="json",
        )
        self.assertEqual(verify.status_code, status.HTTP_200_OK)
        self.assertTrue(CustomUser.objects.get(id=user_id).is_verified)

    def test_login_rejects_bad_password(self):
        CustomUser.objects.create_user(
            email="user@example.com",
            mobile_number="9822222222",
            name="User",
            password="secret123",
        )
        response = self.client.post(
            "/auth/login/",
            {"email": "user@example.com", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email_is_rejected(self):
        payload = {
            "email": "dup@example.com",
            "mobile_number": "9833333333",
            "name": "Dup",
            "password": "secret123",
        }
        self.client.post("/auth/register/", payload, format="json")
        response = self.client.post("/auth/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
