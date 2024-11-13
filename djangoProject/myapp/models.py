from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField(auto_now_add=True)

    ORDER_STATUS_CHOICES = [
        ('new', 'New'),
        ('in_process', 'In Process'),
        ('sent', 'Sent'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return "order id:" + str(self.id) + " status:" + self.status

    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    def can_fulfill_order(self):
        unavailable_products = self.products.filter(available=False)
        if unavailable_products.exists():
            return False,
        return True

    def clean(self):
        can_fulfill_order,message = self.can_fulfill_order()
        if not can_fulfill_order:
            raise ValidationError(message)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

