from django.urls import path, include

urlpatterns = [
    path('v1/', include('traxler.api.v1')),
]
