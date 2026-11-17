from django.conf import settings
from django.db import models


class Post(models.Model):
    """A single property listing.

    House and land specific details live on the same record because the
    marketplace UI presents every listing as one flat property object.
    """

    class Purpose(models.TextChoices):
        BUY = "BY", "Buy"
        SELL = "SL", "Sell"
        RENT = "RT", "Rent"

    class PropertyType(models.TextChoices):
        HOUSE = "H", "House"
        LAND = "L", "Land"
        APARTMENT = "A", "Apartment"

    class AreaFormat(models.TextChoices):
        TERAI = "TE", "Terai (Bigha / Kattha / Dhur)"
        HILL = "HM", "Hilly (Ropani / Aana / Paisa)"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    purpose = models.CharField(
        max_length=2, choices=Purpose.choices, default=Purpose.SELL
    )
    property_type = models.CharField(
        max_length=1,
        choices=PropertyType.choices,
        default=PropertyType.HOUSE,
    )

    price = models.PositiveBigIntegerField(default=0)

    area_formating = models.CharField(
        max_length=2, choices=AreaFormat.choices, default=AreaFormat.HILL
    )
    area1 = models.PositiveIntegerField(default=0)
    area2 = models.PositiveIntegerField(default=0)
    area3 = models.PositiveIntegerField(default=0)
    road_width = models.PositiveIntegerField(default=0)

    no_of_bedrooms = models.PositiveIntegerField(default=0)
    no_of_bathrooms = models.PositiveIntegerField(default=0)
    no_of_floor = models.PositiveIntegerField(default=0)
    parking_area = models.PositiveIntegerField(default=0)
    facing_side = models.CharField(max_length=20, blank=True, default="")
    built_date = models.DateField(null=True, blank=True)

    street = models.CharField(max_length=80, blank=True, default="")
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=80)
    longitude = models.FloatField()
    latitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "posts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["property_type"]),
            models.Index(fields=["purpose"]),
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def area_unit(self) -> str:
        return (
            "Bigha-Kattha-Dhur"
            if self.area_formating == self.AreaFormat.TERAI
            else "Ropani-Aana-Paisa"
        )

    @property
    def area_display(self) -> str:
        units = (
            ("Bigha", "Kattha", "Dhur")
            if self.area_formating == self.AreaFormat.TERAI
            else ("Ropani", "Aana", "Paisa")
        )
        values = (self.area1, self.area2, self.area3)
        parts = [
            f"{value} {unit}"
            for value, unit in zip(values, units)
            if value
        ]
        return ", ".join(parts) if parts else "0"
