from rest_framework import serializers

from user.models import User
from tax.models import Tax, State, TaxDue


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class TaxDueSerializer(serializers.ModelSerializer):

    total = serializers.ReadOnlyField()
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = TaxDue
        exclude = ('tax', 'id')


class BaseTaxSerializer(serializers.ModelSerializer):

    active_due = TaxDueSerializer()
    sgst = serializers.ReadOnlyField()
    paid = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Tax
        fields = '__all__'


class TaxDetailSerializer(BaseTaxSerializer):

    active_due = TaxDueSerializer(write_only=True)
    history = TaxDueSerializer(many=True, read_only=True)
    view = serializers.HyperlinkedIdentityField(
        'tax:tax-retrieve-update', lookup_field='pk', lookup_url_kwarg='pk'
    )

    def update(self, instance, validated_data):

        active_due_data = validated_data.pop('active_due')

        # First update fields of Tax object
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # Then create a new TaxDue object since we keep track of old ones
        tax_due = TaxDue(tax=instance, active=True)
        for field, value in active_due_data.items():
            setattr(tax_due, field, value)
        tax_due.save()

        return instance

    def create(self, validated_data: dict):
        # make sure taxpayer has role of TAXPAYER
        # & not a higher role
        taxpayer = validated_data['payer']

        active_due_data = validated_data.pop('active_due')
        if taxpayer.role != User.TAXPAYER:
            raise serializers.ValidationError('Selected user must be a taxpayer')

        tax = Tax.objects.create(**validated_data, sgst=taxpayer.info.state.tax)

        tax_due = TaxDue(tax=tax, active=True)
        for field, value in active_due_data.items():
            setattr(tax_due, field, value)
        tax_due.save()

        return tax


class TaxListSerializer(BaseTaxSerializer):

    payer = serializers.StringRelatedField()
    view = serializers.HyperlinkedIdentityField(
        'tax:tax-retrieve', lookup_field='pk', lookup_url_kwarg='pk'
    )
