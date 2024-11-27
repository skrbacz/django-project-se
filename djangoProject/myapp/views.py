from django.http import HttpResponse
from rest_framework import viewsets

from .models import Product, Order, Customer
from .serializers import ProductSerializer, OrderSerializer, CustomerSerializer


def hello_world(request):
    return HttpResponse("Hello, World!")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
