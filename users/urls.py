from django.urls import path

from .views.saved_house import ListSavedHouse, SavedHouseDetail

urlpatterns = [
    path("savedhome/<int:pk>/", ListSavedHouse.as_view(), name="saved-home-list"),
    path(
        "savedhome/<int:userId>/<int:postId>/",
        SavedHouseDetail.as_view(),
        name="saved-home-detail",
    ),
]
