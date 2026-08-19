from rest_framework import serializers
from .models import Arrival


class ArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrival
        fields = ['id', 'event_id', 'timestamp', 'latitude', 'longitude', 'device_id', 'event_type', 'duration_seconds']
        read_only_fields = ['id', 'timestamp']
