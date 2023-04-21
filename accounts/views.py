from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView



class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        mobile_number = request.data.get("mobile_number", "")
        name = request.data.get("name", "")
        password = request.data.get("password", "")
        if not email or not name or not password:
            return Response(
                data={
                    "message": "email, name, and password are required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = CustomUser.objects.create_user(
            email=email, 
            mobile_number=mobile_number,
            name=name, 
            password=password
        )
        return Response(
            data=CustomUserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )

class LoginUserView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        
        user = CustomUser.objects.filter(email=email).first()
        user = get_object_or_404(CustomUser,email=email)
        if user:
            if user.check_password(password):
                return Response(
                    data=CustomUserSerializer(user).data,
                    status=status.HTTP_200_OK
                )
        return Response(
            data={
                "message": "Invalid credentials. Try again."
            },
            status=status.HTTP_400_BAD_REQUEST
        )



class UserDetail(generics.RetrieveAPIView):
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer




# def my_view(request): 
#     request.user


class getUserInfoByAccessToken(APIView):

    def post(self,request):
        token = request.data.pop("access_token")
        access_token = AccessToken(access_token)
        return Response(access_token['user_id'])


