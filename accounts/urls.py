from django.urls import path
from .views import RegisterUserView, LoginUserView,UserDetail,getUserInfoByAccessToken

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginUserView.as_view(), name='login'),
    path('users/<int:pk>/', UserDetail.as_view(),name="user-info"),
    path("auth/token/",getUserInfoByAccessToken.as_view())
        

]