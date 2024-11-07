from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField(auto_now_add=True)

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return "order id:" + str(self.id) + " status:" + self.status
