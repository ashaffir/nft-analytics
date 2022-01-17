from email import message
import requests
import logging
import plotly.graph_objects as go
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import TemplateView
from urllib3 import Retry

from .serializers import CollectionSerializer
from opensea.models import (
    OPENSEA_COLLECTIONS_URL,
    OPENSEA_COLLECTION_URL,
    OPENSEA_ASSET_URL,
    OPENSEA_ASSETS_URL,
    Collection,
    CollectionStats,
)

logger = logging.getLogger(__file__)

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
}


class HomeView(TemplateView):
    template_name = "main/home.html"

    def post(self, request):
        context = {}
        data_selector = request.POST.get("data_selector")
        collection_slug = request.POST.get("collection_slug")
        asset_owner = request.POST.get("asset_owner")
        limit = request.POST.get("limit") if request.POST.get("limit") else 1

        # Data selector options
        #######################
        if data_selector == "assets":
            params = {}
            if asset_owner:
                params["owner"] = (asset_owner,)

            if collection_slug:
                params["collection"] = collection_slug

            params["limit"] = limit

            response = requests.get(OPENSEA_ASSETS_URL, params=params, headers=HEADERS)
            context["assets"] = response.json()

        elif data_selector == "collections":
            offset = 0

            if asset_owner:
                get_collections_url = f"{OPENSEA_COLLECTIONS_URL}?asset_owner={asset_owner}&offset={offset}&limit={limit}"
                response = requests.get(get_collections_url)
                context["collections"] = response.json()

            elif collection_slug:
                get_collection_url = f"{OPENSEA_COLLECTION_URL}/{collection_slug}"
                response = requests.get(get_collection_url)
                if response.status_code == 200:
                    collection = response.json()
                    context["collection"] = collection
                else:
                    messages.error(request, "Collection not found")
                    return redirect(request.META["HTTP_REFERER"])

                try:
                    track_collection = self.request.POST.get("track")

                    # Check if this collection is already tracked
                    try:
                        tracked_collection = Collection.objects.get(
                            slug=collection_slug
                        )
                        if tracked_collection.tracked:
                            messages.warning(
                                request,
                                f"Collection {tracked_collection} already being tracked",
                            )
                        else:
                            tracked_collection.tracked = True
                            tracked_collection.save()
                            messages.success(
                                request,
                                f"Collection {tracked_collection} was successfully added to the tracked list",
                            )

                        return redirect(request.META["HTTP_REFERER"])

                    except:
                        logger.info(f"Tracking collection {collection_slug}")
                        context["tracked"] = track_collection

                        # Saving to Database
                        collection_info = {}
                        collection_info["name"] = collection["collection"]["name"]
                        collection_info["slug"] = collection["collection"]["slug"]
                        collection_info["editors"] = collection["collection"]["editors"]
                        collection_info["created"] = collection["collection"][
                            "created_date"
                        ]

                        try:
                            collection_info["address"] = collection["collection"][
                                "primary_asset_contracts"
                            ][0]["address"]
                        except:
                            collection_info["address"] = None

                        collection_info["tracked"] = True

                        try:
                            new_tracked_collection = Collection.objects.create(
                                **collection_info
                            )
                            messages.success(
                                request,
                                f"Collection {new_tracked_collection.name} is currently tracked",
                            )
                        except Exception as e:
                            logger.error(f"Failed creating collection. Error: {e}")
                            messages.error(
                                request,
                                f"Failed creating tracked collection.",
                            )

                except:
                    pass
            else:
                messages.warning(
                    request,
                    "Please enter filter for collections (owner or collection slug",
                )
                return redirect(request.META["HTTP_REFERER"])

        else:
            messages.warning(request, "No data selected")
            return redirect(request.META["HTTP_REFERER"])

        return render(request, "main/home.html", context=context)


from opensea.tasks import poll_tracked_collections


class TrackedCollectionsView(TemplateView):
    """Display the tracked collections"""

    template_name = "main/tracked_collections.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tracked_collections = Collection.objects.filter(tracked=True)
        context["tracked_collection"] = tracked_collections
        return context

    def post(self, request):
        # Testing trackers
        poll_tracked_collections()
        messages.success(request, "Polling success")
        return redirect(request.META["HTTP_REFERER"])


class CollectionStatsView(TemplateView):
    """Dicplay collection stats"""

    template_name = "main/collection_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_slug = kwargs["collection_slug"]
        try:
            collection = Collection.objects.get(slug=collection_slug)
            stats = CollectionStats.objects.filter(collection=collection)
            last_stats = list(stats)[-1]
            context["stats"] = last_stats

            # Graph
            x = [str(stat.created) for stat in stats]
            y = [str(stat.floor_price) for stat in stats]

            trace1 = go.Scatter(
                x=x,
                y=y,
                marker={"color": "red", "symbol": 104, "size": 10},
                mode="lines",
                name="Floor Price",
            )

            x2 = [str(stat.created) for stat in stats]
            y2 = [str(stat.num_owners) for stat in stats]

            trace2 = go.Scatter(
                x=x2,
                y=y2,
                marker={"color": "blue", "symbol": 104, "size": 10},
                mode="lines",
                name="Number of Owners",
            )
            layout = go.Layout(
                title=collection.name,
                xaxis={"title": "Created"},
                # yaxis={"title": "Floor Price"},
            )
            figure = go.Figure(data=[trace1, trace2], layout=layout)

            context["graph"] = figure.to_html()

        except Exception as e:
            logger.error(f"Error getting collection {collection_slug} for stats: {e}")
        return context


from django.conf import settings


class CollectionTransactionsView(TemplateView):
    """Display collection transaction data based on data pulled from Etherscan"""

    template_name = "main/collection_txs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = Collection.objects.get(slug=kwargs["collection_slug"])
        if collection.address != []:
            # Extract data from Etherscan
            EHTERSCAN_API_URL = (
                "https://api.etherscan.io/api?module=account&action=txlist"
            )

            params = {}
            response = requests.get(
                f"{EHTERSCAN_API_URL}&address={collection.address}&startblock=0&endblock=99999999&page=1&offset=0&sort=asc&apikey={settings.ETHERSCAN_API_KEY}"
            )
            if response.status_code == 200:
                context["transactions"] = response.json()
                context["collection"] = collection
            else:
                messages.error(self.request, f"Faild getting Etherscan trasnactions.")
                logger.error(
                    self.request,
                    f"Faild getting Etherscan trasnactions. Error: {response.content}",
                )
        return context


def delete_collection(request, collection_slug):
    """Deleting collection from the tracked list"""
    try:
        collection = Collection.objects.get(slug=collection_slug)
    except Exception as e:
        logger.error(f"Colleciton not found for deletion. Error: {e}")
        messages(request, f"Failed deleting the colleciton.")
        return redirect(request.META["HTTP_REFERER"])

    collection.tracked = False
    collection.save()

    return redirect(request.META["HTTP_REFERER"])
