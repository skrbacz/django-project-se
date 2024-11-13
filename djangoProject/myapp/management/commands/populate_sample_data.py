from decimal import Decimal
from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Clear all previous data
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        # Create product objects (validation happens automatically here)
        product1 = Product.objects.create(
            name="7-pack of silver rings",
            price=19.99,
            available=True
        )
        product2 = Product.objects.create(
            name="Gold earrings",
            price=150.99,
            available=True
        )
        product3 = Product.objects.create(
            name="Gold necklace",
            price=18.99,
            available=True
        )
        product4 = Product.objects.create(
            name="5-pack of silver rings",
            price=7.99,
            available=True
        )

        # Create customer objects (validation happens automatically here)
        customer1 = Customer.objects.create(
            name="Łukasz Stecyk",
            address="ul. Kamienna 135/13, Wrocław 50-045"
        )
        customer2 = Customer.objects.create(
            name="Nikola Różycka",
            address="ul. Stanisława Drabika 73/7, Wrocław 52-131"
        )
        customer3 = Customer.objects.create(
            name="Maja Ludwińska",
            address="ul. Sportowa 5, Ligota Piękna 55-114"
        )
        customer4 = Customer.objects.create(
            name="Oliwia Skrobacz",
            address="ul. Św.Mikołaja 45, Ostrzeszów 63-500"
        )
        customer5 = Customer.objects.create(
            name="Ania Cieplik",
            address="ul. Irlandzka 5/2, Wrocław 54-402"
        )

        order1 = Order.objects.create(
            customer=customer1
        )
        order2 = Order.objects.create(
            customer=customer2
        )
        order3 = Order.objects.create(
            customer=customer3
        )
        order4 = Order.objects.create(
            customer=customer4
        )
        order5 = Order.objects.create(
            customer=customer5
        )

        order1.products.add(product1)
        order2.products.add(product2)
        order3.products.add(product3)
        order4.products.add(product4)
        order5.products.add(product2)

        self.stdout.write("Data created successfully.")
