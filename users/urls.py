from django.urls import path
from .views import ListSavedHouse,SavedHouseDetail

urlpatterns = [
    path('savedhome/<int:pk>', ListSavedHouse.as_view(), name='savedHomeList'),
    path('savedhome/<int:userId>/<int:postId>', SavedHouseDetail.as_view(), name='savedHomeDetail'),
    #  path('addrecommendation/', RecommendationDetail.as_view(), name='recommendation'),
    #  path('recommendation/<int:id>/', ListRecommendation.as_view(), name='recommendation'),
]