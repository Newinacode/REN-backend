from django.urls import path

from .views.OTP import CreateOTPForEmail, VerifyOTP
from .views.user import (
    LoginUserView,
    RegisterUserView,
    UserDetail,
    UserList,
    getUserInfoByAccessToken,
)

urlpatterns = [
    path("auth/register/", RegisterUserView.as_view(), name="register"),
    path("auth/login/", LoginUserView.as_view(), name="login"),
    path("users/", UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetail.as_view(), name="user-info"),
    path("auth/token/", getUserInfoByAccessToken.as_view(), name="auth-token-info"),
    path("auth/sendotp/<int:pk>/", CreateOTPForEmail.as_view(), name="send-otp"),
    path("auth/verifyotp/<int:pk>/", VerifyOTP.as_view(), name="verify-otp"),
]
