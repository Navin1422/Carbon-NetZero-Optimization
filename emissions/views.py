from rest_framework import viewsets
from .models import EmissionLog
from .serializers import EmissionLogSerializer

class EmissionLogViewSet(viewsets.ModelViewSet):
    queryset = EmissionLog.objects.all().order_by('-timestamp')
    serializer_class = EmissionLogSerializer
