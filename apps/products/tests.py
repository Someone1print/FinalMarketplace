"""Тесты каталога: категории, товары, корзина, заказ."""
from decimal import Decimal

from django.test import TestCase

from apps.products.models import Cart, Category, Order, Product
from apps.users.models import Customer, Vendor


class CatalogTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vendor = Vendor.objects.create_user(
            email='vendor@example.com', password='StrongPass123',
            name='Продавец', second_name='Тестовый', phone_number='+996700000002',
        )
        cls.category = Category.objects.create(name='Электроника')
        cls.customer = Customer.objects.create_user(
            email='customer@example.com', password='StrongPass123',
            name='Покупатель', second_name='Тестовый', phone_number='+996700000003',
            cart_number='4169000000000001', address='Бишкек', post_code='720000',
        )

    def make_product(self, name='Наушники', price=1500):
        return Product.objects.create(
            name=name, vendor=self.vendor, category=self.category,
            description='Описание', price=price, url='https://example.com/p/1',
        )


class ProductModelTests(CatalogTestCase):
    def test_product_belongs_to_vendor_and_category(self):
        product = self.make_product()
        self.assertEqual(product.vendor, self.vendor)
        self.assertEqual(product.category, self.category)
        self.assertEqual(self.vendor.product_set.count(), 1)

    def test_deleting_category_removes_products(self):
        self.make_product()
        self.category.delete()
        self.assertEqual(Product.objects.count(), 0)


class CartTests(CatalogTestCase):
    def test_cart_holds_multiple_products(self):
        cart = Cart.objects.create(customer=self.customer)
        first = self.make_product('Наушники', 1500)
        second = self.make_product('Клавиатура', 2500)
        cart.product.add(first, second)
        self.assertEqual(cart.product.count(), 2)

    def test_one_cart_per_customer(self):
        Cart.objects.create(customer=self.customer)
        with self.assertRaises(Exception):
            Cart.objects.create(customer=self.customer)


class OrderTests(CatalogTestCase):
    def test_order_with_products_and_total(self):
        order = Order.objects.create(total_price=Decimal('4000.00'))
        order.products.add(self.make_product('Наушники', 1500))
        order.products.add(self.make_product('Клавиатура', 2500))
        self.assertEqual(order.products.count(), 2)
        self.assertEqual(order.total_price, Decimal('4000.00'))
