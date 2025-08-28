from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    AdminTokenObtainPairSerializer,
    BarberOrderSerializer,
    CocktailOrderSerializer,
    ExpenseSerializer,
)
from .models import BarberOrder, CocktailOrder, Expense


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

    # Ensure proper response to CORS preflight and OPTIONS introspection
    def options(self, request, *args, **kwargs):
        response = Response(status=200)
        # Allow methods for this endpoint
        response["Allow"] = "POST, OPTIONS"
        # CORS headers (django-cors-headers also sets these globally; we add explicitly)
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept, Origin, X-Requested-With"
        response["Access-Control-Allow-Credentials"] = "true"
        # If you want to mirror the Origin, rely on corsheaders; otherwise use '*'
        response["Access-Control-Max-Age"] = "86400"
        return response


class IsStaffOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))


class BarberOrderViewSet(viewsets.ModelViewSet):
    queryset = BarberOrder.objects.all()
    serializer_class = BarberOrderSerializer
    permission_classes = [IsStaffOnly]


class CocktailOrderViewSet(viewsets.ModelViewSet):
    queryset = CocktailOrder.objects.all()
    serializer_class = CocktailOrderSerializer
    permission_classes = [IsStaffOnly]


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsStaffOnly]
