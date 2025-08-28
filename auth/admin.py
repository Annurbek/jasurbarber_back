from django.contrib import admin
from .models import BarberOrder, CocktailOrder, Expense


@admin.register(BarberOrder)
class BarberOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "service_name", "barber_name", "amount")
    search_fields = ("date", "service_name", "barber_name", "amount")


@admin.register(CocktailOrder)
class CocktailOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "service_name", "number_stol", "amount")
    search_fields = ("date", "service_name", "number_stol", "amount")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "description", "amount")
    search_fields = ("date", "description", "amount")
