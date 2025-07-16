from rest_framework import viewsets, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime

from .models import Department, EmissionLog
from .serializers import DepartmentSerializer, EmissionLogSerializer


# ✅ ViewSet for Department (CRUD)
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# ✅ ViewSet for Emission Logs (CRUD)
class EmissionLogViewSet(viewsets.ModelViewSet):
    queryset = EmissionLog.objects.all().order_by('-timestamp')
    serializer_class = EmissionLogSerializer


# ✅ Add a single emission log
@api_view(['POST'])
def add_emission_log(request):
    serializer = EmissionLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# ✅ List emissions (optionally filtered by department)
@api_view(['GET'])
def list_emissions(request):
    department_name = request.GET.get('department')
    if department_name:
        logs = EmissionLog.objects.filter(department__name=department_name)
    else:
        logs = EmissionLog.objects.all()
    serializer = EmissionLogSerializer(logs, many=True)
    return Response(serializer.data)


# ✅ Upload emissions via file (future support)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_emissions(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'No file received'}, status=status.HTTP_400_BAD_REQUEST)

    # 📌 Future: use pandas to read CSV/XLSX and insert EmissionLog entries
    return Response({'message': 'File received successfully'}, status=200)


# ✅ Carbon usage statistics (total + grouped by department)
@api_view(['GET'])
def carbon_usage_stats(request):
    logs = EmissionLog.objects.all()
    total = logs.aggregate(total_emission=Sum('amount'))['total_emission'] or 0

    department_data = (
        logs.values('department__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    return Response({
        "total_emissions": total,
        "by_department": department_data,
    })


# ✅ AI Recommendation (Static for now)
@api_view(['GET'])
def ai_recommendations(request):
    department = request.GET.get('department', 'Boiler')
    return Response({
        "department": department,
        "recommendation": "Switch to solar-assisted heating to reduce CO2 emissions by 20%."
    })


# ✅ Department Progress Over Time
@api_view(['GET'])
def department_progress(request, department_name):
    """
    Return logs for a given department (for progress chart).
    """
    logs = EmissionLog.objects.filter(department__name=department_name).order_by('timestamp')
    serializer = EmissionLogSerializer(logs, many=True)
    return Response({
        "department": department_name,
        "data": serializer.data
    })
