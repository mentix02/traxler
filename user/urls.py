from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path(
        'token/',
        views.ObtainAuthTokenAPIView.as_view(),
        name='token',
    ),
    path(
        'usernames/',
        views.TaxpayerIdListAPIView.as_view(),
        name='usernames',
    ),
    path(
        'taxpayers/',
        views.TaxpayerListCreateAPIView.as_view(),
        name='taxpayer-list-create',
    ),
    path(
        'taxpayers/<str:username>/',
        views.TaxpayerRetrieveUpdateAPIView.as_view(),
        name='taxpayer-retrieve-update',
    ),
]
