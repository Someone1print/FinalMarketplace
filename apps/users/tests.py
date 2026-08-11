"""Тесты кастомной модели пользователя и CustomUserManager."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.users.models import Customer, Vendor

User = get_user_model()


class CustomUserManagerTests(TestCase):
    def test_create_user_normalizes_email_and_hashes_password(self):
        user = User.objects.create_user(email='Buyer@EXAMPLE.com', password='StrongPass123')
        self.assertEqual(user.email, 'Buyer@example.com')
        self.assertNotEqual(user.password, 'StrongPass123')
        self.assertTrue(user.check_password('StrongPass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_without_email_fails(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='StrongPass123')

    def test_create_superuser_sets_flags(self):
        admin = User.objects.create_superuser(email='admin@example.com', password='StrongPass123')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_with_is_staff_false_fails(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='bad@example.com', password='StrongPass123', is_staff=False,
            )

    def test_email_is_unique(self):
        User.objects.create_user(email='dup@example.com', password='StrongPass123')
        with self.assertRaises(Exception):
            User.objects.create_user(email='dup@example.com', password='OtherPass456')


class UserSubtypesTests(TestCase):
    def test_vendor_is_user_subtype(self):
        vendor = Vendor.objects.create_user(
            email='shop@example.com', password='StrongPass123',
            name='Айбек', second_name='Шопов', phone_number='+996700000000',
        )
        self.assertTrue(User.objects.filter(pk=vendor.pk).exists())

    def test_customer_creation(self):
        customer = Customer.objects.create_user(
            email='client@example.com', password='StrongPass123',
            name='Дмитрий', second_name='Клиентов', phone_number='+996700000001',
            cart_number='4169000000000000', address='Бишкек', post_code='720000',
        )
        self.assertEqual(customer.email, 'client@example.com')
