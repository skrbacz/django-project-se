from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    price = models.FloatField()
    available = models.BooleanField(default=False)
