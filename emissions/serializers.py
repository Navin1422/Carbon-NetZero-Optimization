from rest_framework import serializers
from .models import EmissionLog

class EmissionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionLog
        fields = '__all__'
