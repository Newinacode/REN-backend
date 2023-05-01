from django.urls import path
from .views import PostDetailView,PostListView,PostSearchByArea

urlpatterns = [
    path('post/', PostListView.as_view(), name='register'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='login'),
    path('post/search/',PostSearchByArea.as_view(),name="search")
]