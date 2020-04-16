from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

class TrackingViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingSerializer

    def get_queryset(self):
        queryset = Tracking.objects.all()
        return queryset
