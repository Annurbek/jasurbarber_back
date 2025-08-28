from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import BarberOrder, CocktailOrder, Expense


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not (user.is_staff or user.is_superuser):
            raise serializers.ValidationError('Only admin/staff users can log in here.')

        # Extra user info for the client
        data.update({
            'user': {
                'id': user.id,
                'username': user.get_username(),
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
        })
        return data


class BarberOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberOrder
        fields = ['id', 'date', 'service_name', 'barber_name', 'amount']


class CocktailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailOrder
        fields = ['id', 'date', 'service_name', 'number_stol', 'amount', 'status']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'date', 'description', 'amount']
