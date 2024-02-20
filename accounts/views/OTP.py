from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import status
from ..models.OTP import OTP
from ..models.user import CustomUser
from rest_framework.views import APIView
from django.core.mail import send_mail
import random


class CreateOTPForEmail(APIView): 
    def get(self,request,pk):
        user = CustomUser.objects.get(id=pk)
        otp = OTP(user=user,opt_number=random.randint(0,99999))
        otp.save()
        sub = "OTP"
        msg = f"Your OTP is {otp.otp_number}"
        # send_mail(
        #     sub,msg,"realestatenepalkathford@gmail.com",[user.email]
        # )
        return Response(data={
            "message":"OTP sent to signup email"
        },            status=status.HTTP_201_CREATED)


class VerifyOTP(APIView): 
    def post(self,request,pk):
        sent_otp = request.data.get("otp")
        print(sent_otp)
        user = CustomUser.objects.get(id=pk)
        print(user)
        otp = OTP.objects.get(user=user)
        valid_otp = otp.otp_number 
        print(valid_otp)
        print(valid_otp==int(sent_otp))
        if(valid_otp==int(sent_otp)):
            user.is_verified = True
            user.save()
            return Response(data={
                "message":"Valid OTP"},status=status.HTTP_200_OK) 
        return Response(  
                data={
                "message":"Invalid OTP",},status=status.HTTP_401_UNAUTHORIZED

        )
