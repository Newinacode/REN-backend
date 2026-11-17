from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.user import CustomUser
from posts.models.post import Post
from posts.serializers.post import PostSerializer

from ..models.saved_house import SavedHome
from ..serializers.saved_house import SavedHouseSerializer


def _ensure_owner(request, user_id):
    return request.user.id == user_id or request.user.is_staff


class ListSavedHouse(APIView):
    """GET /savedhome/<user_id>/ - all listings saved by a user."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        if not _ensure_owner(request, pk):
            return Response(
                {"message": "You can only view your own saved listings."},
                status=status.HTTP_403_FORBIDDEN,
            )

        saved_posts = (
            Post.objects.filter(saved_by__user_id=pk)
            .select_related("author")
            .prefetch_related("images")
            .order_by("-saved_by__created_at")
        )
        serializer = PostSerializer(
            saved_posts, many=True, context={"request": request}
        )
        return Response(serializer.data)


class SavedHouseDetail(APIView):
    """GET / POST / DELETE /savedhome/<user_id>/<post_id>/"""

    permission_classes = (IsAuthenticated,)

    def get(self, request, userId, postId, format=None):
        if not _ensure_owner(request, userId):
            return Response(status=status.HTTP_403_FORBIDDEN)
        saved_home = SavedHome.objects.filter(
            user_id=userId, post_id=postId
        ).first()
        if saved_home is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            SavedHouseSerializer(saved_home, context={"request": request}).data
        )

    def post(self, request, userId, postId, format=None):
        if not _ensure_owner(request, userId):
            return Response(
                {"message": "You can only save listings to your own account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        get_object_or_404(CustomUser, pk=userId)
        get_object_or_404(Post, pk=postId)
        saved_home, created = SavedHome.objects.get_or_create(
            user_id=userId, post_id=postId
        )
        return Response(
            SavedHouseSerializer(saved_home).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def delete(self, request, userId, postId, format=None):
        if not _ensure_owner(request, userId):
            return Response(status=status.HTTP_403_FORBIDDEN)
        SavedHome.objects.filter(user_id=userId, post_id=postId).delete()
        return Response(
            {"message": "Saved listing removed."}, status=status.HTTP_200_OK
        )
