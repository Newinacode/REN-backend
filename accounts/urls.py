from django.urls import path
from .views import RegisterUserView, LoginUserView,UserDetail,getUserInfoByAccessToken,CreateOptForEmail,VerifyOPT

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginUserView.as_view(), name='login'),
    path('users/<int:pk>/', UserDetail.as_view(),name="user-info"),
    path("auth/token/",getUserInfoByAccessToken.as_view()),
    path("auth/sendopt/<int:pk>",CreateOptForEmail.as_view()),
    path("auth/verifyopt/<int:pk>",VerifyOPT.as_view())
       
        

]