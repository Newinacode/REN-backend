from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from ..models.user import CustomUser
from ..serializers.user import CustomUserSerializer


def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }


class RegisterUserView(generics.CreateAPIView):
    """POST /auth/register/"""

    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Account created. Verify your email with the OTP.",
                    "user": CustomUserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Could not create the account.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginUserView(APIView):
    """POST /auth/login/"""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""

        if not email or not password:
            return Response(
                {"message": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request=request, email=email, password=password)
        if not user:
            return Response(
                {"message": "Invalid credentials. Try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.is_active:
            return Response(
                {"message": "This account has been disabled."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "message": "Logged in successfully.",
                "user": CustomUserSerializer(user).data,
                "is_verified": user.is_verified,
                **tokens_for(user),
            },
            status=status.HTTP_200_OK,
        )


class IsSelfOrAdmin(BasePermission):
    """A user may only read their own profile unless they are staff."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.id == request.user.id


class UserDetail(generics.RetrieveAPIView):
    """GET /users/<pk>/"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, IsSelfOrAdmin)


class UserList(generics.ListAPIView):
    """GET /users/ (staff only)"""

    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)


class getUserInfoByAccessToken(APIView):
    """POST /auth/token/  { "access_token": "..." }"""

    permission_classes = (AllowAny,)

    def post(self, request):
        raw_token = request.data.get("access_token")
        if not raw_token:
            return Response(
                {"message": "access_token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = AccessToken(raw_token)
            user = CustomUser.objects.get(id=token["user_id"])
        except (TokenError, KeyError, CustomUser.DoesNotExist):
            return Response(
                {"message": "Invalid or expired token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(CustomUserSerializer(user).data)
