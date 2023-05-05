from django.shortcuts import render
from rest_framework.views import APIView
from .models import SavedHome,Recommendation
from .serializers import SavedHouseSerializer
from posts.serializers import PostSerializer
from accounts.models import CustomUser
from rest_framework.response import Response
from posts.models import Post
from rest_framework.views import status
from django.shortcuts import get_object_or_404
import pandas as pd
from sklearn.neighbors import NearestNeighbors


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




class ListRecommendation(APIView):
    def get(self,request,id,format=None):
        id = get_object_or_404(CustomUser,pk=id)
        recommended_posts = Recommendation.objects.filter(user=id)
        recommended_list = []
        for i in recommended_posts:
            recommended_list.append(recommended_list.append(i.post.id))

        post_list = Post.objects.filter(id__in = recommended_list)
        posts = PostSerializer(post_list,many=True)
        return Response(posts.data)

class RecommendationDetail(APIView): 

    def post(self,request,format=None):
        user_id = request.data["user"]
        post_id = request.data['post']

        features = ["price", "no_of_bedrooms", "no_of_bathrooms", "no_of_floor", "parking_area"]

        df = pd.read_csv('updated_data3.csv')
        df.fillna(0, inplace=True)
        df_norm = (df[features] - df[features].mean()) / df[features].std()
        knn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
        knn_model.fit(df_norm)


        def get_recommendations(query):
            features = ["price", "no_of_bedrooms", "no_of_bathrooms", "no_of_floor", "parking_area",]
            query_df = pd.DataFrame(query, index=[0])
            query_norm = (query_df[features] - df[features].mean()) / df[features].std()
            distances, indices = knn_model.kneighbors(query_norm)
            recommended_properties = df.loc[indices[0]][["id","title"]]
            return recommended_properties

        user = CustomUser.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        query = {"price": post.price, "no_of_bedrooms": post.no_of_bedrooms, "no_of_bathrooms": post.no_of_bathrooms, "no_of_floor": post.no_of_floor, "parking_area": post.parking_area}
        recommended_properties = get_recommendations(query)
        for i in recommended_properties["id"]:
            post = Post.objects.get(id=i)
            recommendation = Recommendation(user=user,post=post)
            recommendation.save()



        return Response(status=status.HTTP_200_OK)

    


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



