from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from ..models.user import CustomUser
from ..serializers.user import CustomUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from django.core.mail import send_mail

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data = request.data)
        data = {}
        response_status = ''
        if serializer.is_valid():
            new_user = serializer.save()
            print(new_user)
            data = {
                "data":CustomUserSerializer(new_user).data,
                "message":"User has been created Successfully"
            }
            response_status = status.HTTP_201_CREATED
            
        else: 
            data = {
                "message":serializer.errors
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response (
            data = data, 
            status = response_status
        )


class LoginUserView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        
        # user = CustomUser.objects.filter(email=email).first()
        # user = get_object_or_404(CustomUser,email=email)
        user = authenticate(email=email, password=password)
        
        data = {}
        print("here")

        if user:
            # if user.check_password(password):
            #     RefreshToken
            refresh = RefreshToken.for_user(user)
            data = {
                "user" : CustomUserSerializer(user).data,
                "token":{
                    "refresh_token":str(refresh),
                    "access_token":str(refresh.access_token)
                },
                "message": "Login Sucessfully"
            }

            return Response(
                data=data,
                status=status.HTTP_200_OK
            )
        else:
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
