import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.OTP import OTP
from ..models.user import CustomUser


class CreateOTPForEmail(APIView):
    """GET /auth/sendotp/<pk> - create and email a one time password."""

    permission_classes = (AllowAny,)

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)

        # Keep one active OTP per user.
        OTP.objects.filter(user=user).delete()
        otp = OTP.objects.create(
            user=user, otp_number=random.randint(100000, 999999)
        )

        message = (
            f"Hello {user.name},\n\n"
            f"Your Real Estate Nepal verification code is {otp.otp_number}.\n"
            "It expires when you request a new one.\n"
        )
        send_mail(
            "Your REN verification code",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

        payload = {"message": "OTP sent to the signup email."}
        # The console email backend is used in development, so expose the
        # code to make the flow testable. This is hidden when DEBUG=False.
        if settings.DEBUG:
            payload["dev_otp"] = otp.otp_number
        return Response(payload, status=status.HTTP_201_CREATED)


class VerifyOTP(APIView):
    """POST /auth/verifyotp/<pk>  { "otp": "123456" }"""

    permission_classes = (AllowAny,)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        otp = OTP.objects.filter(user=user).order_by("-id").first()

        if otp is None:
            return Response(
                {"message": "No OTP found. Request a new code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            sent_otp = int(request.data.get("otp"))
        except (TypeError, ValueError):
            return Response(
                {"message": "Enter the numeric OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if sent_otp != otp.otp_number:
            return Response(
                {"message": "Invalid OTP."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user.is_verified = True
        user.save(update_fields=["is_verified"])
        OTP.objects.filter(user=user).delete()
        return Response(
            {"message": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )
