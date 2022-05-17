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

    active_due = TaxDueSerializer()
    payer_name = serializers.SerializerMethodField()
    history = TaxDueSerializer(many=True, read_only=True)

    # noinspection PyMethodMayBeStatic
    def get_payer_name(self, obj: Tax):
        return f'{obj.payer.get_full_name()} ({obj.payer.username})'

    def update(self, instance, validated_data):

        # Make sure the user who is updating the tax is not a taxpayer
        if self.context['request'].user.role <= User.TAXPAYER:
            raise serializers.ValidationError(
                'Only tax accountants or admins can update taxes'
            )

        try:
            active_due_data = validated_data.pop('active_due')
        except KeyError:
            active_due_data = None

        # First update fields of Tax object
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # No active_due_data was provided, return instance
        if active_due_data is None:
            return instance

        # Create a new TaxDue object since we keep track of old ones
        tax_due = TaxDue(tax=instance, active=True)
        for field, value in active_due_data.items():
            setattr(tax_due, field, value)
        tax_due.save()

        return instance

    def create(self, validated_data: dict):

        # Make sure the user who is creating the tax is not a taxpayer
        if self.context['request'].user.role <= User.TAXPAYER:
            raise serializers.ValidationError(
                'Only tax accountants or admins can create taxes'
            )

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
