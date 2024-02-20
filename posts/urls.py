from django.urls import path
from .views.post import PostDetailView,PostView,PostSearchByArea

urlpatterns = [
    path('', PostView.as_view(), name='add-post'),
    path('<int:pk>/', PostDetailView.as_view(), name='login'),
    path('search/',PostSearchByArea.as_view(),name="search")
]