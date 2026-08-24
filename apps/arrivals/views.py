import math

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import CharField
from django.db.models.functions import Cast
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Arrival
from .serializers import ArrivalSerializer

_POI_LAT = -2.132459
_POI_LNG = -79.906834
_POI_RADIUS_M = 6

PAGE_SIZE = 20


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
        lat_q = self.request.GET.get('lat', '').strip()
        lng_q = self.request.GET.get('lng', '').strip()
        near_poi_filter = self.request.GET.get('poi') == '1'
        page_num = self.request.GET.get('page', 1)

        qs = Arrival.objects.all()

        if near_poi_filter:
            # Bounding-box pre-filter in DB (0.0002° ≈ 22 m), then exact haversine in Python
            delta = 0.0002
            candidates = list(
                qs.filter(
                    latitude__gte=_POI_LAT - delta,
                    latitude__lte=_POI_LAT + delta,
                    longitude__gte=_POI_LNG - delta,
                    longitude__lte=_POI_LNG + delta,
                )
            )
            paginatable = [
                e for e in candidates
                if _haversine_m(e.latitude, e.longitude, _POI_LAT, _POI_LNG) <= _POI_RADIUS_M
            ]
            for e in paginatable:
                e.near_poi = True
            paginator = Paginator(paginatable, PAGE_SIZE)
            page_obj = paginator.get_page(page_num)
        else:
            if lat_q or lng_q:
                qs = qs.annotate(
                    lat_str=Cast('latitude', output_field=CharField()),
                    lng_str=Cast('longitude', output_field=CharField()),
                )
                if lat_q:
                    qs = qs.filter(lat_str__contains=lat_q)
                if lng_q:
                    qs = qs.filter(lng_str__contains=lng_q)

            paginator = Paginator(qs, PAGE_SIZE)
            page_obj = paginator.get_page(page_num)
            for event in page_obj:
                event.near_poi = (
                    _haversine_m(event.latitude, event.longitude, _POI_LAT, _POI_LNG) <= _POI_RADIUS_M
                )

        context['events'] = page_obj
        context['page_obj'] = page_obj
        context['lat_q'] = lat_q
        context['lng_q'] = lng_q
        context['near_poi_filter'] = near_poi_filter
        context['total_enters'] = Arrival.objects.filter(event_type=Arrival.ENTER).count()
        context['total_exits'] = Arrival.objects.filter(event_type=Arrival.EXIT).count()
        context['total_stationary'] = Arrival.objects.filter(event_type=Arrival.STATIONARY).count()
        context['poi_lat'] = _POI_LAT
        context['poi_lng'] = _POI_LNG
        context['poi_radius_m'] = _POI_RADIUS_M
        return context
