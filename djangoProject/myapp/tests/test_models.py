from decimal import Decimal

from django.db import IntegrityError, DataError
from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):

    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertEqual(temp_product.available, True)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Temporary product', price=-1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_no_name(self):
        with self.assertRaises(IntegrityError):
            temp_product = Product.objects.create(name=None, price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_available_field(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99)
        self.assertEqual(temp_product.available, False)

    def test_create_product_with_edge_name_length_maximum(self):
        temp_product = Product.objects.create(name='a' * 150, price=1.99, available=True)
        self.assertEqual(temp_product.name, 'a' * 150)
        self.assertEqual(temp_product.price, 1.99)
        self.assertEqual(temp_product.available, True)

    def test_create_product_with_edge_name_length_minimum(self):
        temp_product = Product.objects.create(name='a', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'a')
        self.assertEqual(temp_product.price, 1.99)
        self.assertEqual(temp_product.available, True)

    def test_create_product_with_edge_name_too_long(self):
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(name='a' * 151, price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_name_too_short(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='', price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_duplicate_name(self):
        Product.objects.create(name='Temporary product', price=1.99, available=True)
        with self.assertRaises(IntegrityError):
            Product.objects.create(name='Temporary product', price=2.99, available=True)

    def test_create_product_with_edge_price_minimum(self):
        temp_product = Product.objects.create(name='Temporary product', price=0.01, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 0.01)
        self.assertEqual(temp_product.available, True)

    def test_create_product_with_edge_price_maximum(self):
        temp_product = Product.objects.create(name='Temporary product', price=999999.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 999999.99)
        self.assertEqual(temp_product.available, True)

    def test_create_product_with_price_exceeded(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Temporary product', price=1000000.01, available=True)
            temp_product.full_clean()

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Temporary product', price=1.9999, available=True)
            temp_product.full_clean()


class CustomerModelTest(TestCase):

    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='Temporary customer', address='Temporary address')
        self.assertEqual(temp_customer.name, 'Temporary customer')
        self.assertEqual(temp_customer.address, 'Temporary address')

    def test_create_customer_with_no_address(self):
        with self.assertRaises(IntegrityError):
            temp_customer = Customer.objects.create(name='Temporary customer', address=None)
            temp_customer.full_clean()

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='Temporary customer', address='')
            temp_customer.full_clean()

    def test_create_customer_with_edge_name_length_maximum(self):
        temp_customer = Customer.objects.create(name='a' * 100, address='Temporary address')
        self.assertEqual(temp_customer.name, 'a' * 100)
        self.assertEqual(temp_customer.address, 'Temporary address')

    def test_create_customer_with_edge_name_length_minimum(self):
        temp_customer = Customer.objects.create(name='a', address='Temporary address')
        self.assertEqual(temp_customer.name, 'a')
        self.assertEqual(temp_customer.address, 'Temporary address')

    def test_create_customer_with_edge_name_too_long(self):
        with self.assertRaises(DataError):
            temp_customer = Customer.objects.create(name='a' * 101, address='Temporary address')
            temp_customer.full_clean()

    def test_create_customer_with_name_too_short(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='', address='Temporary address')
            temp_customer.full_clean()

    def test_create_customer_with_no_name(self):
        with self.assertRaises(IntegrityError):
            temp_customer = Customer.objects.create(name=None, address='Temporary address')
            temp_customer.full_clean()


class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(name='Temporary customer', address='Temporary address')
        self.product1 = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.product2 = Product.objects.create(name='Product temporary', price=99.10, available=True)

    def test_create_order_with_valid_data(self):
        temp_order = Order.objects.create(customer=self.customer)
        temp_order.products.add(self.product1, self.product2)
        self.assertEqual(temp_order.customer, self.customer)
        self.assertEqual(list(temp_order.products.all()), [self.product1, self.product2])
        self.assertEqual(temp_order.status, 'new')

    def test_create_order_with_no_customer(self):
        with self.assertRaises(IntegrityError):
            temp_order = Order.objects.create(customer=None)
            temp_order.products.add(self.product1, self.product2)
            temp_order.full_clean()

    def test_total_price_calculation_with_products(self):
        temp_order = Order.objects.create(customer=self.customer)
        temp_order.products.add(self.product1, self.product2)
        self.assertEqual(temp_order.calculate_total_price(), Decimal('101.09'))

    def test_total_price_calculation_with_no_products(self):
        temp_order = Order.objects.create(customer=self.customer)
        self.assertEqual(temp_order.calculate_total_price(), 0)

    def test_order_can_be_fulfilled(self):
        temp_order = Order.objects.create(customer=self.customer)
        temp_order.products.add(self.product1, self.product2)
        self.assertEqual(temp_order.can_be_fulfilled(), True)

    def test_create_order_with_at_least_one_product_unavailable(self):
        unavailable_product = Product.objects.create(name='Unavailable product', price=99.99, available=False)
        temp_order = Order.objects.create(customer=self.customer)
        temp_order.products.add(self.product1, unavailable_product)
        self.assertEqual(temp_order.can_be_fulfilled(), False)

    def test_create_order_with_missing_status(self):
        temp_order = Order.objects.create(customer=self.customer)
        self.assertEqual(temp_order.status, 'new')

    def test_create_order_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            temp_order = Order.objects.create(customer=self.customer, status='invalid_status')
            temp_order.full_clean()
