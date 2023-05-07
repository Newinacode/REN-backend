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
from sklearn.preprocessing import LabelEncoder
import numpy as np

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

        # features = ["price", "no_of_bedrooms", "no_of_bathrooms", "no_of_floor", "parking_area"]

        # df = pd.read_csv('updated_data3.csv')
        # df.fillna(0, inplace=True)
        # df_norm = (df[features] - df[features].mean()) / df[features].std()
        # knn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
        # knn_model.fit(df_norm)


        # def get_recommendations(query):
        #     features = ["price", "no_of_bedrooms", "no_of_bathrooms", "no_of_floor", "parking_area",]
        #     query_df = pd.DataFrame(query, index=[0])
        #     query_norm = (query_df[features] - df[features].mean()) / df[features].std()
        #     distances, indices = knn_model.kneighbors(query_norm)
        #     recommended_properties = df.loc[indices[0]][["id","title"]]
        #     return recommended_properties

        # user = CustomUser.objects.get(id=user_id)
        # post = Post.objects.get(id=post_id)
        # query = {"price": post.price, "no_of_bedrooms": post.no_of_bedrooms, "no_of_bathrooms": post.no_of_bathrooms, "no_of_floor": post.no_of_floor, "parking_area": post.parking_area}
        # recommended_properties = get_recommendations(query)

        user = CustomUser.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        knn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
        df = pd.read_csv('updated_data3.csv')
        encoder = LabelEncoder()
        features = ["property_type","purpose"]
        df["property_type"] = encoder.fit_transform(df["property_type"])
        df["purpose"] = encoder.fit_transform(df["purpose"])
        df_norm=df[features]
        one_hot=pd.get_dummies(df['city'])
        df_norm=pd.concat([df_norm,one_hot],axis=1)
        knn_model.fit(df_norm)
        retQuery=np.zeros((1,34))


        def get_Que(query):
            retQuery=np.zeros((1,34))
            if(query['purpose']=='SL'):
                retQuery[0][0]=1
            if(query["property_type"]=='H'):
                retQuery[0][1]=1

            c=np.array(['Bara', 'Bardiya', 'Bhairahawa', 'Bhaktapur', 'Biratnagar',
            'Birtamod', 'Butwal', 'Chitwan', 'Dang', 'Dhading', 'Dharan',
            'Illam', 'Itahari', 'Jhapa', 'Kailali', 'Kapilvastu', 'Kaski',
            'Kathmandu', 'Kavre', 'Kirtipur', 'Lalitpur', 'Mahottari',
            'Makwanpur', 'Morang', 'Nawalparasi', 'Nawalpur', 'Parsa',
            'Pokhara', 'Rupandehi', 'Sunsari', 'Surkhet', 'Tanahu'],
            dtype=object)
            retQuery[0][2+np.where(c==query["city"])[0][0]]=1
            distances, indices=knn_model.kneighbors(retQuery)
            return indices

        query = {"property_type":post.property_type,"purpose":post.purpose,"city":post.city}
        ids=get_Que(query)
        recommended_properties = df.loc[ids[0]][["id","title","location"]]


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



