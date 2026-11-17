from math import atan2, cos, radians, sin, sqrt

from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from ..models.post import Post
from ..models.post_image import PostImage
from ..serializers.post import PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow anyone to read a listing, only its author to change it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            obj.author_id == request.user.id or request.user.is_staff
        )


def _as_float(value, default=None):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def distance_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points in kilometres."""
    radius = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return radius * 2 * atan2(sqrt(a), sqrt(1 - a))


class PostViewSet(viewsets.ModelViewSet):
    """CRUD API for property listings plus search and recommendations."""

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("author")
            .prefetch_related("images")
            .all()
        )
        params = self.request.query_params

        purpose = params.get("purpose")
        if purpose:
            queryset = queryset.filter(purpose=purpose)

        property_type = params.get("property_type") or params.get("type")
        if property_type:
            queryset = queryset.filter(property_type=property_type.upper()[:1])

        city = params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)

        author = params.get("author")
        if author:
            queryset = queryset.filter(author_id=author)

        search = params.get("q")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(location__icontains=search)
                | Q(city__icontains=search)
                | Q(content__icontains=search)
            )

        min_price = _as_float(params.get("min_price"))
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        max_price = _as_float(params.get("max_price"))
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        ordering = params.get("ordering")
        allowed_ordering = {
            "price",
            "-price",
            "created_at",
            "-created_at",
            "no_of_bedrooms",
            "-no_of_bedrooms",
        }
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        self._save_uploaded_images(post)

    def perform_update(self, serializer):
        post = serializer.save()
        self._save_uploaded_images(post)

    def _save_uploaded_images(self, post):
        files = list(self.request.FILES.getlist("uploaded_images"))
        files += list(self.request.FILES.getlist("images"))
        for uploaded_file in files:
            if uploaded_file:
                PostImage.objects.create(post=post, images=uploaded_file)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def mine(self, request):
        posts = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(posts)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(posts, many=True).data)

    @action(
        detail=False,
        methods=["get", "post"],
        permission_classes=(permissions.AllowAny,),
    )
    def search(self, request):
        data = request.data if request.method == "POST" else request.query_params
        queryset = Post.objects.select_related("author").prefetch_related("images").all()

        property_type = (data.get("type") or "").lower()
        type_map = {"house": "H", "land": "L", "apartment": "A"}
        if property_type in type_map:
            queryset = queryset.filter(property_type=type_map[property_type])

        purpose = data.get("purpose")
        if purpose in dict(Post.Purpose.choices):
            queryset = queryset.filter(purpose=purpose)

        city = data.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)

        search = data.get("q")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(location__icontains=search)
                | Q(city__icontains=search)
            )

        bedroom = _as_float(data.get("bedroom"))
        if bedroom:
            queryset = queryset.filter(no_of_bedrooms__gte=int(bedroom))

        min_price = _as_float(data.get("min_price"))
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        max_price = _as_float(data.get("max_price"))
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        results = list(queryset)

        # Area filters only make sense within the same unit system.
        area_format = data.get("area_formating")
        minimum_area = (
            int(_as_float(data.get("area1"), 0) or 0),
            int(_as_float(data.get("area2"), 0) or 0),
            int(_as_float(data.get("area3"), 0) or 0),
        )
        if area_format in dict(Post.AreaFormat.choices):
            results = [p for p in results if p.area_formating == area_format]
        if any(minimum_area):
            results = [
                p
                for p in results
                if (p.area1, p.area2, p.area3) >= minimum_area
            ]

        latitude = _as_float(data.get("latitude"))
        longitude = _as_float(data.get("longitude"))
        radius = _as_float(data.get("radius"))
        if (
            latitude is not None
            and longitude is not None
            and radius is not None
            and radius > 0
        ):
            nearby = []
            for post in results:
                km = distance_km(latitude, longitude, post.latitude, post.longitude)
                if km <= radius:
                    nearby.append((km, post))
            nearby.sort(key=lambda item: item[0])
            results = [post for _, post in nearby]

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recommendations(self, request):
        """Recommendations for the signed-in user.

        Uses the cities/purposes of saved listings. Falls back to the newest
        listings when there is not enough signal (e.g. a brand new account).
        """
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        saved = list(
            request.user.saved_homes.select_related("post").values_list(
                "post_id", flat=True
            )
        )
        saved_posts = Post.objects.filter(id__in=saved)
        cities = set(saved_posts.values_list("city", flat=True))
        purposes = set(saved_posts.values_list("purpose", flat=True))

        base = Post.objects.select_related("author").prefetch_related("images")

        recommended = []
        if cities or purposes:
            query = Q()
            if cities:
                query |= Q(city__in=cities)
            if purposes:
                query |= Q(purpose__in=purposes)
            recommended = list(
                base.filter(query)
                .exclude(id__in=saved)
                .exclude(author=request.user)
                .order_by("-created_at")[:8]
            )

        if len(recommended) < 8:
            seen = {post.id for post in recommended} | set(saved)
            fill = (
                base.exclude(id__in=seen)
                .exclude(author=request.user)
                .order_by("-created_at")[: 8 - len(recommended)]
            )
            recommended.extend(fill)

        return Response(self.get_serializer(recommended, many=True).data)
