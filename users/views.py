from django.shortcuts import render
from rest_framework.views import APIView
from .models import SavedHome
from .serializers import SavedHouseSerializer
from accounts.models import CustomUser
from rest_framework.response import Response
from posts.models import Post
from rest_framework.views import status
from django.shortcuts import get_object_or_404


class ListSavedHouse(APIView): 

    def get(self,request,pk,format=None): 
        user = CustomUser.objects.get(pk=pk)
        savedhome = SavedHome.objects.filter(user=pk)
        serializer = SavedHouseSerializer(savedhome,many=True)
        return Response(serializer.data)




class SavedHouseDetail(APIView):


    def get(self,request,userId,postId,format=None):
        user = CustomUser.objects.get(pk=userId)
        post = Post.objects.get(pk=postId)
        savedHome = get_object_or_404(SavedHome,user=user,post=post)
        serializer = SavedHouseSerializer(savedHome)
        return Response(serializer.data)

    def post(self,request,userId,postId,format=None): 
        user = CustomUser.objects.get(pk=userId)
        post = Post.objects.get(pk=postId)
        savedHome = SavedHome(user=user,post=post)
        savedHome.save()
        return Response({"message":"post is saved"},status=status.HTTP_201_CREATED)


    def delete(self,request,userId,postId,format=None):
        user = CustomUser.objects.get(pk=userId)
        post = Post.objects.get(pk=postId)
        savedHome = SavedHome.objects.get(user=user,post=post)
        savedHome.delete()
        return Response({"message":"saved post is deleted"},status=status.HTTP_200_OK)



