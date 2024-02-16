from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from .models import CustomUser,OPT
from .serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from django.core.mail import send_mail
import random
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register/
    """
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




class CreateOptForEmail(APIView): 
    def get(self,request,pk):
        user = CustomUser.objects.get(id=pk)
        otp = OPT(user=user,opt_number=random.randint(0,99999))
        otp.save()
        sub = "OTP"
        msg = f"Your OPT is {opt.opt_number}"
        # send_mail(
        #     sub,msg,"realestatenepalkathford@gmail.com",[user.email]
        # )
        return Response(data={
            "message":"OPT sent to signup email"
        },            status=status.HTTP_201_CREATED)


class VerifyOPT(APIView): 
    def post(self,request,pk):
        sent_opt = request.data.get("otp")
        print(sent_opt)
        user = CustomUser.objects.get(id=pk)
        print(user)
        opt = OPT.objects.get(user=user)
        valid_opt = opt.opt_number 
        print(valid_opt)
        print(valid_opt==int(sent_opt))
        if(valid_opt==int(sent_opt)):
            user.is_verified = True
            user.save()
            return Response(data={
                "message":"Valid OPT"},status=status.HTTP_200_OK) 
        return Response(  
                data={
                "message":"Invalid OPT",},status=status.HTTP_401_UNAUTHORIZED

        )
