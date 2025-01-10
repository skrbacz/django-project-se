from django.http import HttpResponse
from rest_framework import viewsets

from .models import Product, Order, Customer
from .serializers import ProductSerializer, OrderSerializer, CustomerSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

from rest_framework.filters import SearchFilter


def hello_world(request):
    return HttpResponse("Hello, World!")


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [SearchFilter,]
    search_fields = ['name']


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
