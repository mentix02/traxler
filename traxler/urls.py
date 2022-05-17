from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('traxler.api')),
    path('drf-auth/', include('rest_framework.urls')),
    path('__debug__', include('debug_toolbar.urls')),
]
