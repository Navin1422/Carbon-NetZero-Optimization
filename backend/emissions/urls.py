from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet,
    EmissionLogViewSet,
    upload_emissions,
    add_emission_log,
    list_emissions,
    carbon_usage_stats,
    ai_recommendations,
    department_progress,
)

# ✅ Registering ViewSets for /departments/ and /logs/
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)  # API: /api/departments/
router.register(r'logs', EmissionLogViewSet)        # API: /api/logs/

# ✅ Combined URLs
urlpatterns = [
    path('', include(router.urls)),  # Include all ViewSet routes
    
    # Custom function-based API endpoints
    path('emissions/', list_emissions),                                 # GET
    path('emissions/add/', add_emission_log),                           # POST
    path('emissions/stats/', carbon_usage_stats),                       # GET
    path('emissions/ai-recommendations/', ai_recommendations),         # GET
    path('emissions/progress/<str:department_name>/', department_progress),  # GET
    path('upload-emissions/', upload_emissions),                        # POST (future)
]
