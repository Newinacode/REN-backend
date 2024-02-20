from django.shortcuts import render
from rest_framework.views import APIView
from ..models.saved_house import SavedHome
from ..serializers.saved_house import SavedHouseSerializer
from posts.serializers.post import PostSerializer
from rest_framework.response import Response
from posts.models.post import Post
from rest_framework.views import status
from django.shortcuts import get_object_or_404
from accounts.models.user import CustomUser


class ListSavedHouse(APIView): 
    def get(self,request,pk,format=None): 
        user = CustomUser.objects.get(pk=pk)
        savedhome = SavedHome.objects.filter(user=pk)
        post_array = []
        for i in savedhome: 
            post_array.append(i.post.id)
        saved_post = Post.objects.filter(id__in = post_array)
        serializer = PostSerializer(saved_post,many=True)
        return Response(serializer.data)




class SavedHouseDetail(APIView):


    def get(self,request,userId,postId,format=None):
        user = CustomUser.objects.get(pk=userId)
        post = Post.objects.get(pk=postId)

        savedHome = SavedHome.objects.filter(user=user,post=post)
        if savedHome: 
            savedHome = savedHome[0]

        else:
                return Response(status=status.HTTP_204_NO_CONTENT)
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



