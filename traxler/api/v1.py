from django.urls import path, include

urlpatterns = [
    path('tax/', include('tax.urls')),
    path('users/', include('user.urls')),
]
