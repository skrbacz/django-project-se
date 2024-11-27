from django.urls import path, include
from .views import hello_world, ProductViewSet,OrderViewSet, CustomerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('api/', include(router.urls)),
]
