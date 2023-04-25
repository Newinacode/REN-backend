from django.shortcuts import render
from .models import Post,PostImage
from .serializers import PostSerializer,PostImageSerializer#,MapSerializer
from rest_framework import mixins,generics,viewsets,serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from property.serializers import HouseSerializer,LandSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser



class PostListView(APIView): 
    parser_classes = (MultiPartParser, )


    def get(self,request,format=None): 
        post = Post.objects.all()
        serializers = PostSerializer(post,many=True)
        return Response(serializers.data)


    def post(self,request,format=None):
        print(request.data)
        uploaded_data = request.FILES.getlist("uploaded_images")
        print(request.data.get('uploaded_images'))
        
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid(): 
            new_data = serializer.save()
            print(uploaded_data)
            for uploaded_item in uploaded_data:
                new_product_image = PostImage.objects.create(post = new_data, images = uploaded_item)
          
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class PostDetailView(APIView):

    def get(self,request,pk,format=None):
        post = get_object_or_404(Post,id=pk)
        serializers = PostSerializer(post)
        return Response(serializers.data)



    def put(self,request,pk,format=None): 
        post = get_object_or_404(Post,id=pk)
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid(): 
            serializers.save()
            return Response(serializers.data)

        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk,format=None): 
        post = get_object_or_404(Post,id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]

    queryset = Post.objects.all()
    serializer_class = PostSerializer



            
    
    # def perform_create(self, serializer):
    #     house_data = dict(self.request.data).pop('house', None)
    #     land_data = dict(self.request.data).pop('land', None)
    #     map_data = dict(self.request.data).pop('map', None)
        
    #     post = serializer.save()
        
    #     house_serializer = HouseSerializer(data=house_data)
    #     land_serializer = LandSerializer(data=land_data)
    #     map_serializer = MapSerializer(data=map_data)
        
    #     if house_serializer.is_valid() and land_serializer.is_valid() and map_serializer.is_valid():
    #         house = house_serializer.save()
    #         land = land_serializer.save()
    #         map = map_serializer.save()
            
    #         post.house = house
    #         post.land = land
    #         post.map = map
    #         post.save()
    #     else:
    #         raise serializers.ValidationError(house_serializer.errors)




@api_view(['PUT'])
def update_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







    






