from django.db.models import Q, Count
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)

from user.models import User
from user.permissions import IsTaxAccountantOrAdmin
from user.serializers import (
    TaxpayerIdSerializer,
    ObtainTokenSerializer,
    ListTaxpayerSerializer,
    UpdateTaxpayerSerializer,
    CreateTaxpayerSerializer,
)


class TaxpayerIdListAPIView(ListAPIView):
    serializer_class = TaxpayerIdSerializer
    permission_classes = (IsTaxAccountantOrAdmin,)
    queryset = User.objects.filter(role=User.TAXPAYER).only('username')


class ObtainAuthTokenAPIView(CreateAPIView):
    queryset = User.objects.none()
    permission_classes = (AllowAny,)
    serializer_class = ObtainTokenSerializer


class TaxpayerListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsTaxAccountantOrAdmin)
    queryset = (
        User.objects.filter(role=User.TAXPAYER)
        .select_related('info', 'info__state')
        .defer(*ListTaxpayerSerializer.Meta.exclude)
        .annotate(
            total_taxes=Count('taxes', distinct=True),
            paid_taxes=Count(
                'taxes',
                distinct=True,
                filter=Q(taxes__paid=True),
            ),
        )
        .order_by('-date_joined')
    )

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTaxpayerSerializer
        return ListTaxpayerSerializer


class TaxpayerRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    lookup_url_kwarg = 'username'
    lookup_field = 'username__exact'
    serializer_class = UpdateTaxpayerSerializer
    queryset = User.objects.filter(role=User.TAXPAYER)
    permission_classes = (IsAuthenticated, IsTaxAccountantOrAdmin)
