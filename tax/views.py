from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)

from tax.models import Tax, State
from tax.serializers import StateSerializer, TaxListSerializer, TaxDetailSerializer
from user.permissions import (
    IsTaxPayer,
    IsTaxAccountantOrAdmin,
    IsTaxAccountantOrAdminOrReadonly,
)


class StateListAPIView(ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class TaxRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = TaxDetailSerializer
    permission_classes = (IsTaxAccountantOrAdmin,)
    queryset = Tax.objects.all().prefetch_related('history').select_related('payer')


class PayTaxAPIView(APIView):

    permission_classes = (IsTaxPayer,)

    @staticmethod
    def post(request, pk):
        tax = get_object_or_404(Tax.objects.filter(payer=request.user), pk=pk)
        tax.paid = True
        tax.save()
        return Response(TaxListSerializer(tax, context={'request': request}).data)


class TaxListCreateAPIView(ListCreateAPIView):

    permission_classes = (IsTaxAccountantOrAdminOrReadonly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaxListSerializer
        return TaxDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == user.TAXPAYER:
            qs = Tax.objects.filter(payer=user)
        else:
            qs = Tax.objects.all()
        return qs.select_related('payer').order_by('-pk')
