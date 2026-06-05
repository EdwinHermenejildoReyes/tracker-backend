from django.urls import path
from .views import ArrivalListCreateView, DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/arrivals/', ArrivalListCreateView.as_view(), name='arrivals'),
]
