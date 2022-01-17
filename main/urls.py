from unicodedata import name
from urllib.parse import urlparse
from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "tracked-collections/",
        views.TrackedCollectionsView.as_view(),
        name="tracked-collections",
    ),
    path(
        "collection-stats/<str:collection_slug>",
        views.CollectionStatsView.as_view(),
        name="collection-stats",
    ),
    path(
        "collection-delete/<str:collection_slug>",
        views.delete_collection,
        name="collection-delete",
    ),
    path(
        "collection-txs/<str:collection_slug>",
        views.CollectionTransactionsView.as_view(),
        name="collection-txs",
    ),
]
