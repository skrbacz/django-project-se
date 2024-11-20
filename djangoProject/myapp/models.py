from django.core.exceptions import ValidationError
from django.db import models
from decimal import Decimal


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.price:
            if self.price != self.price.quantize(Decimal("0.01")):
                raise ValidationError({"price": "Ensure that there are no more than 2 decimal places."})
            if self.price < 0:
                raise ValidationError({"price": "Price cannot be negative."})

    def save(self, *args, **kwargs):
        if isinstance(self.price, float):
            self.price = Decimal(str(self.price))
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

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new')

    def __str__(self):
        return "order id:" + str(self.id) + " status:" + self.status

    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    def can_be_fulfilled(self):
        return all(product.available for product in self.products.all())

