from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('api/swagger/schema/swagger-ui/', SpectacularSwaggerView.as_view(), name='swagger'),
    path('api/swagger/schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),
    path('api/swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', include('api.urls')),
]
