"""Load the bundled property dataset and create demo accounts.

Usage:
    python manage.py seed_data            # skip if listings already exist
    python manage.py seed_data --fresh    # wipe listings and reload
"""

import csv
import re
import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models.user import CustomUser
from posts.models.post import Post
from posts.models.post_image import PostImage
from users.models.saved_house import SavedHome

CSV_PATH = settings.BASE_DIR / "updated_data3.csv"

IMAGE_SOURCES = [
    settings.BASE_DIR.parent / "REN-FRONTEND" / "src" / "assets" / "images" / "home.jpeg",
    settings.BASE_DIR.parent / "REN-FRONTEND" / "src" / "assets" / "images" / "2.jpg",
    settings.BASE_DIR.parent / "REN-FRONTEND" / "src" / "assets" / "images" / "new-house.png",
]

# Fallback map centres used when a row has no usable coordinates.
CITY_CENTRES = {
    "kathmandu": (27.7172, 85.3240),
    "lalitpur": (27.6588, 85.3247),
    "bhaktapur": (27.6710, 85.4298),
    "pokhara": (28.2096, 83.9856),
    "chitwan": (27.5291, 84.3542),
    "makwanpur": (27.4285, 85.0323),
    "nawalparasi": (27.5327, 83.6740),
    "dharan": (26.8065, 87.2846),
}


def as_int(value, default=0):
    if value is None or value == "":
        return default
    if isinstance(value, str):
        match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if not match:
            return default
        value = match.group()
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def as_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_date(value):
    for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except (TypeError, ValueError):
            continue
    return None


class Command(BaseCommand):
    help = "Seed demo users and import property listings from updated_data3.csv"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete existing listings before importing.",
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            admin = self._ensure_user(
                email="admin@ren.local",
                password="admin12345",
                name="REN Admin",
                mobile_number="9800000001",
                is_admin=True,
            )
            demo = self._ensure_user(
                email="demo@ren.local",
                password="demo12345",
                name="Demo User",
                mobile_number="9800000002",
            )

            if options["fresh"]:
                PostImage.objects.all().delete()
                SavedHome.objects.all().delete()
                Post.objects.all().delete()
                self._reset_sequences()
                self.stdout.write("Removed existing listings.")

            if Post.objects.exists():
                self._seed_saved_homes(demo)
                self.stdout.write(
                    self.style.WARNING(
                        "Listings already exist. Use --fresh to reload them."
                    )
                )
                self._print_accounts()
                return

            image_paths = self._copy_seed_images()
            self._import_posts(admin)
            if image_paths:
                # Every demo listing gets one of the bundled photos so the
                # marketplace always has a visual. The files are reused, not
                # copied, so this stays cheap.
                all_posts = list(Post.objects.order_by("id"))
                PostImage.objects.bulk_create(
                    [
                        PostImage(
                            post=post,
                            images=image_paths[index % len(image_paths)],
                        )
                        for index, post in enumerate(all_posts)
                    ],
                    batch_size=500,
                )

            self._seed_saved_homes(demo)

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {Post.objects.count()} property listings.")
        )
        self._print_accounts()

    def _ensure_user(self, email, password, name, mobile_number, is_admin=False):
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "mobile_number": mobile_number,
                "is_admin": is_admin,
                "is_verified": True,
                "is_active": True,
            },
        )
        if created:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user

    def _copy_seed_images(self):
        seed_dir = Path(settings.MEDIA_ROOT) / "seed"
        seed_dir.mkdir(parents=True, exist_ok=True)
        copied = []
        for source in IMAGE_SOURCES:
            if source.exists():
                destination = seed_dir / source.name
                if not destination.exists():
                    shutil.copyfile(source, destination)
                copied.append(f"seed/{source.name}")
        return copied

    def _reset_sequences(self):
        """Restart integer primary keys after a destructive re-seed."""
        from django.db import connection

        if connection.vendor == "sqlite":
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM sqlite_sequence WHERE name IN "
                    "('posts_post', 'posts_postimage', 'users_savedhome')"
                )

    def _import_posts(self, author):
        if not CSV_PATH.exists():
            self.stdout.write(self.style.ERROR(f"Dataset not found: {CSV_PATH}"))
            return []

        posts = []
        with CSV_PATH.open(newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                title = (row.get("title") or "").strip()
                if not title:
                    continue

                property_type = (row.get("property_type") or "H").strip().upper()
                if property_type not in dict(Post.PropertyType.choices):
                    property_type = "H"

                purpose = (row.get("purpose") or "SL").strip().upper()
                if purpose not in dict(Post.Purpose.choices):
                    purpose = "SL"

                area_format = (row.get("area_formating") or "HM").strip().upper()
                if area_format not in dict(Post.AreaFormat.choices):
                    area_format = "HM"

                location = (row.get("location") or row.get("city") or "Nepal").strip()
                city = (row.get("city") or "Kathmandu").strip()
                bedrooms = as_int(row.get("no_of_bedrooms"))
                units = (
                    ("Ropani", "Aana", "Paisa")
                    if area_format == "HM"
                    else ("Bigha", "Kattha", "Dhur")
                )
                area_values = [
                    as_int(row.get("area1")),
                    as_int(row.get("area2")),
                    as_int(row.get("area3")),
                ]
                area_text = (
                    " ".join(
                        f"{value} {unit}"
                        for value, unit in zip(area_values, units)
                        if value
                    )
                    or "0"
                )
                road_width = as_int(row.get("road_width"))

                if property_type == "H":
                    summary = (
                        f"{bedrooms} bedroom house with "
                        f"{as_int(row.get('no_of_bathrooms'))} bathrooms in "
                        f"{city}. Built on {area_text} of land"
                        + (f" with a {road_width} ft road." if road_width else ".")
                    )
                else:
                    summary = (
                        f"{area_text} of land for sale in {city}"
                        + (f", with a {road_width} ft road." if road_width else ".")
                    )

                # The bundled CSV labels its coordinate columns backwards:
                # "latitude" holds the longitude (85.x) and "longitude" holds
                # the latitude (27.x). Normalise both, then fall back to the
                # city centre when a row is missing coordinates.
                raw_lat = as_float(row.get("longitude"), 0.0)
                raw_lng = as_float(row.get("latitude"), 0.0)
                centre = CITY_CENTRES.get(city.lower(), CITY_CENTRES["kathmandu"])
                if not (26.0 <= raw_lat <= 31.0):
                    raw_lat = centre[0]
                if not (80.0 <= raw_lng <= 89.5):
                    raw_lng = centre[1]

                posts.append(
                    Post(
                        author=author,
                        title=title[:255],
                        content=summary,
                        purpose=purpose,
                        property_type=property_type,
                        price=as_int(row.get("price")),
                        area_formating=area_format,
                        area1=as_int(row.get("area1")),
                        area2=as_int(row.get("area2")),
                        area3=as_int(row.get("area3")),
                        road_width=as_int(row.get("road_width")),
                        no_of_bedrooms=bedrooms,
                        no_of_bathrooms=as_int(row.get("no_of_bathrooms")),
                        no_of_floor=as_int(row.get("no_of_floor")),
                        parking_area=as_int(row.get("parking_area")),
                        facing_side=(row.get("facing_side") or "")[:20],
                        built_date=parse_date(row.get("built_date")),
                        street=location.split(",")[0][:80],
                        location=location[:255],
                        city=city[:80],
                        latitude=round(raw_lat, 6),
                        longitude=round(raw_lng, 6),
                    )
                )

        Post.objects.bulk_create(posts, batch_size=500)
        return list(Post.objects.order_by("id"))

    def _seed_saved_homes(self, user):
        if SavedHome.objects.filter(user=user).exists():
            return
        posts = Post.objects.order_by("-created_at")[:3]
        SavedHome.objects.bulk_create(
            [SavedHome(user=user, post=post) for post in posts]
        )

    def _print_accounts(self):
        self.stdout.write("")
        self.stdout.write("Demo accounts:")
        self.stdout.write("  admin@ren.local / admin12345  (Django admin + owner)")
        self.stdout.write("  demo@ren.local  / demo12345   (verified buyer)")
