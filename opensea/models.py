from email.policy import default
from tabnanny import verbose
from django.db import models
from django.forms import DateField, DateTimeField, JSONField

OPENSEA_ASSET_URL = "https://api.opensea.io/api/v1/asset"
OPENSEA_ASSETS_URL = "https://api.opensea.io/api/v1/assets"
OPENSEA_COLLECTIONS_URL = "https://api.opensea.io/api/v1/collections"
OPENSEA_COLLECTION_URL = "https://api.opensea.io/api/v1/collection"


class Collection(models.Model):
    """A Collection object info"""

    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now_add=True)
    editors = models.JSONField(default=list)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    address = models.CharField(max_length=50)
    tracked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self) -> str:
        return self.slug


class CollectionStats(models.Model):
    """A Collection stats"""

    created = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, null=True, blank=True
    )
    one_day_volume = models.FloatField(default=0.0, blank=True)
    one_day_change = models.FloatField(default=0.0, blank=True)
    one_day_sales = models.FloatField(default=0.0, blank=True)
    one_day_average_price = models.FloatField(default=0.0, blank=True)
    seven_day_volume = models.FloatField(default=0.0, blank=True)
    seven_day_change = models.FloatField(default=0.0, blank=True)
    seven_day_sales = models.FloatField(default=0.0, blank=True)
    seven_day_average_price = models.FloatField(default=0.0, blank=True)
    thirty_day_volume = models.FloatField(default=0.0, blank=True)
    thirty_day_change = models.FloatField(default=0.0, blank=True)
    thirty_day_sales = models.FloatField(default=0.0, blank=True)
    thirty_day_average_price = models.FloatField(default=0.0, blank=True)
    total_volume = models.FloatField(default=0.0, blank=True)
    total_sales = models.FloatField(default=0.0, blank=True)
    total_supply = models.FloatField(default=0.0, blank=True)
    count = models.FloatField(default=0.0, blank=True)
    num_owners = models.FloatField(default=0.0, blank=True)
    average_price = models.FloatField(default=0.0, blank=True)
    num_reports = models.FloatField(default=0.0, blank=True)
    market_cap = models.FloatField(default=0.0, blank=True)
    floor_price = models.FloatField(default=0.0, blank=True)

    class Meta:
        verbose_name = "Collection stats"
        verbose_name_plural = "Collections stats"
