from rest_framework import serializers
from .models import Arrival


class ArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrival
        fields = ['id', 'timestamp', 'latitude', 'longitude', 'device_id']
        read_only_fields = ['id', 'timestamp']
