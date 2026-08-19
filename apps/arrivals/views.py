import math

from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Arrival
from .serializers import ArrivalSerializer

_POI_LAT = -2.132459
_POI_LNG = -79.906834
_POI_RADIUS_M = 20


def _haversine_m(lat1, lng1, lat2, lng2):
    R = 6_371_000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        if not settings.TRACKER_API_KEY:
            return True
        return request.headers.get('X-API-Key') == settings.TRACKER_API_KEY


class ArrivalListCreateView(generics.ListCreateAPIView):
    queryset = Arrival.objects.all()
    serializer_class = ArrivalSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [HasAPIKey()]
        return []

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        if event_id:
            try:
                existing = Arrival.objects.get(event_id=event_id)
                return Response(ArrivalSerializer(existing).data, status=status.HTTP_200_OK)
            except Arrival.DoesNotExist:
                pass
        return super().create(request, *args, **kwargs)


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = list(Arrival.objects.all()[:100])
        for event in events:
            event.near_poi = (
                _haversine_m(event.latitude, event.longitude, _POI_LAT, _POI_LNG) <= _POI_RADIUS_M
            )
        context['events'] = events
        context['total_enters'] = Arrival.objects.filter(event_type=Arrival.ENTER).count()
        context['total_exits'] = Arrival.objects.filter(event_type=Arrival.EXIT).count()
        context['total_stationary'] = Arrival.objects.filter(event_type=Arrival.STATIONARY).count()
        context['poi_lat'] = _POI_LAT
        context['poi_lng'] = _POI_LNG
        context['poi_radius_m'] = _POI_RADIUS_M
        return context
