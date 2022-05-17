from django.urls import path

from tax import views

app_name = 'tax'

urlpatterns = [
    path(
        'pay/<int:pk>/',
        views.PayTaxAPIView.as_view(),
        name='pay',
    ),
    path(
        'states/',
        views.StateListAPIView.as_view(),
        name='state-list',
    ),
    path(
        'taxes/',
        views.TaxListCreateAPIView.as_view(),
        name='tax-list-create',
    ),
    path(
        'taxes/view/<int:pk>/',
        views.TaxRetrieveUpdateAPIView.as_view(),
        name='tax-retrieve-update',
    ),
]
