from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.permissions import BasePermission

from .models import Arrival
from .serializers import ArrivalSerializer


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


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['arrivals'] = Arrival.objects.all()[:100]
        context['total'] = Arrival.objects.count()
        return context
