from rest_framework import viewsets
from ptkt.api import serializers
from ptkt import models

class PtktViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PtktSerializer
    queryset = models.Tickets.objects.all()