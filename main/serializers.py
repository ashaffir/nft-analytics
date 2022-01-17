from rest_framework import serializers

from opensea.models import Collection, CollectionStats


class CollectionSerializer(serializers.ModelSerializer):
    """Seralizer for the collection info from the OpenSea API"""

    class Meta:
        model = Collection
        fields = "__all__"


class CollectionStatsSerializer(serializers.ModelSerializer):
    """Seralizer for the collection stats from the OpenSea API"""

    class Meta:
        model = CollectionStats
        # fields = "__all__"
        exclude = ("collection",)
