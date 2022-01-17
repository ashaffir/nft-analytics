from django.contrib import admin

from .models import Collection, CollectionStats


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "updated",
        "slug",
        "address",
        "tracked",
    )
    search_fields = (
        "name",
        "slug",
        "address",
    )
    ordering = ("-created",)


@admin.register(CollectionStats)
class CollectionStatsAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "collection",
        "count",
        "floor_price",
        "num_owners",
    )

    search_fields = ("collection",)

    list_filter = ("collection",)

    ordering = ("-created",)
