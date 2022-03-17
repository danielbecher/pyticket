from rest_framework import serializers
from ptkt import models

class PtktSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tickets
        fields = '__all__'