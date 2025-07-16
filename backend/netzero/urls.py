from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Optional: Custom homepage for root "/"
def home(request):
    return HttpResponse("✅ Welcome to the Carbon Net Zero Backend! Use /api/ to access the emissions API.")

urlpatterns = [
    path('', home),                          # Shows a basic welcome message at root
    path('admin/', admin.site.urls),         # Django admin panel
    path('api/', include('emissions.urls')), # API endpoints for emissions app
]
