from django.shortcuts import get_object_or_404

from rest_framework import serializers

from user.models import User, Info as UserInfo


class TaxpayerIdSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = User
        fields = ('id', 'username', 'name')


class ObtainTokenSerializer(serializers.ModelSerializer):

    role = serializers.ReadOnlyField()
    username = serializers.CharField(required=True)
    token = serializers.StringRelatedField(read_only=True, source='auth_token')
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = get_object_or_404(User, username__exact=username)
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'token', 'role')


class CreateTaxpayerSerializer(serializers.ModelSerializer):

    role = serializers.ReadOnlyField()
    token = serializers.StringRelatedField(read_only=True, source='auth_token')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = (
            'role',
            'token',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )


class ListUserInfoSerializer(serializers.ModelSerializer):

    state = serializers.StringRelatedField()

    class Meta:
        model = UserInfo
        exclude = ('user', 'id')


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        exclude = ('user', 'id')


class BaseTaxpayerSerializer(serializers.ModelSerializer):

    paid_taxes = serializers.SerializerMethodField()
    total_taxes = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    view = serializers.HyperlinkedIdentityField(
        'user:taxpayer-retrieve-update',
        lookup_field='username',
        lookup_url_kwarg='username',
    )

    # noinspection PyMethodMayBeStatic
    def get_total_taxes(self, obj):
        if hasattr(obj, 'total_taxes'):
            return obj.total_taxes
        return obj.taxes.count()

    # noinspection PyMethodMayBeStatic
    def get_paid_taxes(self, obj):
        if hasattr(obj, 'paid_taxes'):
            return obj.paid_taxes
        return obj.taxes.filter(paid=True).count()

    class Meta:
        model = User
        exclude = (
            'password',
            'is_superuser',
            'is_staff',
            'is_active',
            'role',
            'groups',
            'user_permissions',
            'last_login',
        )


class UpdateTaxpayerSerializer(BaseTaxpayerSerializer):

    info = UpdateUserInfoSerializer()

    def update(self, instance: User, validated_data: dict):
        info = instance.info
        instance.username = validated_data.pop('username')

        # Update info fields
        for field, value in validated_data.pop('info').items():
            setattr(info, field, value)

        # Update user fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        info.save()
        instance.save()

        return instance


class ListTaxpayerSerializer(BaseTaxpayerSerializer):
    info = ListUserInfoSerializer(read_only=True)
