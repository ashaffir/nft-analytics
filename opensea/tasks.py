from asyncio.log import logger
import logging
import time
import requests
from celery import shared_task
from .models import (
    Collection,
    CollectionStats,
    OPENSEA_COLLECTION_URL,
)

from main.serializers import CollectionStatsSerializer

logger = logging.getLogger(__file__)


@shared_task
def poll_tracked_collections():
    tracked_collections = Collection.objects.filter(tracked=True)
    for collection in tracked_collections:
        logger.info(f"Retrieving collection: {collection.slug}")
        get_collection_url = f"{OPENSEA_COLLECTION_URL}/{collection.slug}"
        res = requests.get(get_collection_url)
        if res.status_code == 200:
            try:
                collection_json = res.json()
                data = collection_json["collection"]["stats"]
                data["collection"] = collection
                serializer = CollectionStatsSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                CollectionStats.objects.create(**data)

            except Exception as e:
                logger.error(f"Failed saving stats. Error: {e}")
                logger.error(f"Failed saving collection stats. ERROR: {res.content}")
        else:
            logger.error(f"Failed saving collection stats. ERROR: {res.content}")

        # Avoid Opensea requests restrictions
        time.sleep(0.5)


@shared_task
def checkcheck():
    print(f"Tracking........")
