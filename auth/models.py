from django.db import models

class BarberOrder(models.Model):
    # All fields stored as text as requested
    date = models.CharField(max_length=100, help_text="Date of the service (text)")
    service_name = models.CharField(max_length=255, help_text="Service name (text)")
    barber_name = models.CharField(max_length=255, help_text="Barber name (text)")
    amount = models.CharField(max_length=100, help_text="Service amount/price (text)")

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.date} - {self.service_name} - {self.barber_name} - {self.amount}"


class Expense(models.Model):
    # All fields as text except description which can be longer
    date = models.CharField(max_length=100, help_text="Date of the expense (text)")
    description = models.TextField(help_text="What this expense was for")
    amount = models.CharField(max_length=100, help_text="Expense amount (text)")

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.description[:30]}"


class CocktailOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reject', 'Reject'),
        ('ready', 'Ready'),
        ('accepted', 'Accepted'),
    ]
    date = models.CharField(max_length=100, help_text="Date of the order (text)")
    service_name = models.CharField(max_length=255, help_text="Cocktail/drink name (text)")
    number_stol = models.IntegerField(help_text="Table number (integer)")
    amount = models.CharField(max_length=100, help_text="Price/amount (text)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', help_text="Order status")

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.date} - {self.service_name} - {self.number_stol} - {self.amount} - {self.status}"