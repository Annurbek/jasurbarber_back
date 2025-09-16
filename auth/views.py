from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import (
    AdminTokenObtainPairSerializer,
    BarberOrderSerializer,
    CocktailOrderSerializer,
    ExpenseSerializer,
)
from .models import BarberOrder, CocktailOrder, Expense
from rest_framework.views import APIView
import requests
from django.conf import settings


@method_decorator(csrf_exempt, name='dispatch')
class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer
    authentication_classes = []  # Disable authentication classes for this view
    permission_classes = []  # Disable permission classes for this view

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


class ComplaintView(APIView):
    def post(self, request):
        full_name = request.data.get('fullName')
        phone = request.data.get('phone')
        message = request.data.get('message')

        # Compose the message for Telegram
        text = f"📝 Yangi shikoyat:\n\n👤 Ism: {full_name}\n📞 Telefon: {phone}\n💬 Xabar: {message}"

        # Telegram bot config
        TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
        TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': text
        }

        try:
            resp = requests.post(url, data=payload)
            if resp.status_code == 200:
                return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'error': 'Telegram error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
