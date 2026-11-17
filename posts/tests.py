import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.user import CustomUser

from .models.post import Post


def listing_payload(**overrides):
    payload = {
        "title": "Test house in Baneshwor",
        "content": "A comfortable three bedroom house.",
        "purpose": "SL",
        "property_type": "H",
        "price": 12000000,
        "area_formating": "HM",
        "area1": 2,
        "area2": 4,
        "area3": 0,
        "no_of_bedrooms": 3,
        "no_of_bathrooms": 2,
        "no_of_floor": 2,
        "parking_area": 1,
        "facing_side": "East",
        "street": "Baneshwor",
        "location": "Baneshwor, Kathmandu",
        "city": "Kathmandu",
        "latitude": 27.6899,
        "longitude": 85.3425,
    }
    payload.update(overrides)
    return payload


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PostApiTests(APITestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            email="owner@example.com",
            mobile_number="9844444444",
            name="Owner",
            password="secret123",
        )
        self.other = CustomUser.objects.create_user(
            email="other@example.com",
            mobile_number="9855555555",
            name="Other",
            password="secret123",
        )
        self.client.force_authenticate(self.owner)

    def test_create_and_read_listing(self):
        create = self.client.post("/post/", listing_payload(), format="json")
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        post_id = create.data["id"]
        self.assertEqual(create.data["author"], self.owner.id)

        detail = self.client.get(f"/post/{post_id}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["area_display"], "2 Ropani, 4 Aana")

        listing = self.client.get("/post/")
        self.assertEqual(listing.status_code, status.HTTP_200_OK)
        self.assertEqual(listing.data["count"], 1)

    def test_create_listing_with_uploaded_image(self):
        buffer = BytesIO()
        Image.new("RGB", (4, 4), "green").save(buffer, format="JPEG")
        upload = SimpleUploadedFile(
            "house.jpg", buffer.getvalue(), content_type="image/jpeg"
        )

        response = self.client.post(
            "/post/",
            {**listing_payload(), "uploaded_images": [upload]},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["images"]), 1)
        self.assertIn("/media/", response.data["images"][0]["image_url"])

    def test_anonymous_can_read_but_not_create(self):
        post = Post.objects.create(author=self.owner, **listing_payload())
        self.client.force_authenticate(user=None)

        self.assertEqual(self.client.get("/post/").status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.get(f"/post/{post.id}/").status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            self.client.post("/post/", listing_payload(), format="json").status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_only_owner_can_update_or_delete(self):
        create = self.client.post("/post/", listing_payload(), format="json")
        post_id = create.data["id"]

        self.client.force_authenticate(self.other)
        forbidden = self.client.patch(
            f"/post/{post_id}/", {"title": "Hijacked"}, format="json"
        )
        self.assertEqual(forbidden.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.owner)
        update = self.client.patch(
            f"/post/{post_id}/", {"title": "Updated title"}, format="json"
        )
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        self.assertEqual(update.data["title"], "Updated title")

        delete = self.client.delete(f"/post/{post_id}/")
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post_id).exists())

    def test_search_filters_by_type_city_and_bedrooms(self):
        self.client.post("/post/", listing_payload(), format="json")
        self.client.post(
            "/post/",
            listing_payload(
                title="Land in Pokhara",
                property_type="L",
                city="Pokhara",
                no_of_bedrooms=0,
                latitude=28.2096,
                longitude=83.9856,
            ),
            format="json",
        )

        response = self.client.post(
            "/post/search/",
            {"type": "house", "city": "Kathmandu", "bedroom": 3},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["property_type"], "H")

    def test_saved_home_flow(self):
        post = Post.objects.create(author=self.owner, **listing_payload())

        save = self.client.post(f"/savedhome/{self.owner.id}/{post.id}/")
        self.assertEqual(save.status_code, status.HTTP_201_CREATED)
        self.assertEqual(save.data["post"], post.id)

        listing = self.client.get(f"/savedhome/{self.owner.id}/")
        self.assertEqual(listing.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listing.data), 1)

        other_view = self.client.get(f"/savedhome/{self.other.id}/")
        self.assertEqual(other_view.status_code, status.HTTP_403_FORBIDDEN)

        remove = self.client.delete(f"/savedhome/{self.owner.id}/{post.id}/")
        self.assertEqual(remove.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(f"/savedhome/{self.owner.id}/").data, [])

    def test_recommendations_require_authentication(self):
        Post.objects.create(author=self.owner, **listing_payload())
        self.client.force_authenticate(user=None)
        response = self.client.get("/post/recommendations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.owner)
        response = self.client.get("/post/recommendations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
