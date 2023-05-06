from django.shortcuts import render
from .models import Post,PostImage
from .serializers import PostSerializer#SearchResultSerializer,PostImageSerializer#,MapSerializer
from rest_framework import mixins,generics,viewsets,serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from math import radians, sin, cos, sqrt, atan2
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



class PostListView(APIView): 
    parser_classes = (MultiPartParser, )
    # permission_classes = [IsAuthenticated]



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
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk,format=None): 
        post = get_object_or_404(Post,id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the Earth in kilometers

    # convert latitude and longitude coordinates from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # calculate the differences between the latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # apply the Haversine formula to calculate the distance
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance





class PostSearchByArea(APIView):

    def post(self,request,format=None): 
        paginator = PageNumberPagination()

        result = Post.objects.all()

        
        longitude = float(request.data["longitude"])
        latitude = float(request.data["latitude"])
        radius = float(request.data["radius"])



        
       

       
        if request.data["area1"]:
            print("got here")
            area1 =request.data["area1"]
            result = result.filter(area1__gte=area1)

        if request.data["area2"]:
            area2 =request.data["area2"]
            result = result.filter(area2__gte=area2)
    
        if request.data["area3"]:
            area1 =request.data["area3"]
            result = result.filter(area3__gte=area3)
            

        if request.data["type"]:
            if request.data["type"]=="house":
                type = request.data["type"]
                result = result.filter(property_type="H")
                if request.data["bedroom"]: 
                    bedroom = int(request.data["bedroom"])
                    print(result)
                    result = result.filter(no_of_bedrooms__gte=bedroom)
            elif request.data["type"] == "land": 
                result = result.filter(property_type="L")
        area1 = request.data["area1"] 
        area2 = request.data["area2"] 
        area3 = request.data["area3"]

        print(result)
        if longitude and latitude and radius:
            result = [res for res in result if distance(longitude,latitude,res.latitude,res.longitude)<=radius]
        
        print(len(result))


        serializers = PostSerializer(result,many=True)
        paginated_data = paginator.paginate_queryset(serializers.data, request)

        
        return Response(paginated_data)


        


        
      
        


        

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
    







    






