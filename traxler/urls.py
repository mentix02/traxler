from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include, re_path

index_view = TemplateView.as_view(template_name='index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('traxler.api')),
    path('drf-auth/', include('rest_framework.urls')),
    path('__debug__', include('debug_toolbar.urls')),
    path('', index_view),
    re_path(r'^.*', index_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
