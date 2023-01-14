from django.shortcuts import render
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from rest_framework import mixins
from rest_framework import generics



'''
This class methods will handle the get and post request. 
Create Post and get list of all Post.
'''

class PostList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView): 
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self,request,*args,**kwargs): 
        return self.list(request,*args,**kwargs)
    

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

'''
This class methods will handle the individual/particular post functionality like to delete,modify/update.
'''

class PostDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView): 
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)    


    











# To list the all post
# class PostList(generics.ListCreateAPIView): 
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# To retrive,update or delete the particular post
# class PostDetail(generics.RetrieveUpdateDestroyAPIView): 
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer