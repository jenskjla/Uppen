# course_generator/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('content.urls')),  # Prefix API endpoints with /api/
]

# Print all registered URLs for debugging
from django.urls import get_resolver

for url_pattern in get_resolver().url_patterns:
    print(url_pattern)
