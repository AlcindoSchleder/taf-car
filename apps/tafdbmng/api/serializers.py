"""taf_car Serializer



"""

from rest_framework import serializers
from apps.tafdbmng.models import Freights


class FreightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Freights
        fields = ['pk_freights']
