from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductEndpointTests(TestCase):
	def test_get_products_returns_valid_products(self):
		Product.objects.create(name='Notebook', price='1250.00', stock=3)

		response = self.client.get(reverse('get_products'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()[0]['price'], '1250.00')

	def test_create_product_rejects_invalid_decimal(self):
		response = self.client.post(
			reverse('create_product'),
			data={'name': 'Invalid', 'price': '100000000', 'stock': '1'},
			content_type='application/json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Product.objects.count(), 0)
