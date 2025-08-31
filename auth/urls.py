from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AdminTokenObtainPairView, BarberOrderViewSet, CocktailOrderViewSet, ExpenseViewSet
from .views import ComplaintView  # add this import

router = DefaultRouter()
router.register(r'barber-orders', BarberOrderViewSet, basename='barber-order')
router.register(r'cocktail-orders', CocktailOrderViewSet, basename='cocktail-order')
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('admin/login/', AdminTokenObtainPairView.as_view(), name='admin_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('complaint/', ComplaintView.as_view(), name='complaint'),  # add this line
    path('', include(router.urls)),
]
