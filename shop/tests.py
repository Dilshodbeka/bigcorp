from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Category, Product, ProductProxy


class ProductViewTest(TestCase):
    def test_get_products(self):

        small_giff = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
        )
        uploaded = SimpleUploadedFile('test_image.gif', small_giff, content_type='image/gif')
        category = Category.objects.create(name='django')
        product_1 = Product.objects.create(
            title = 'Product 1', category=category, image=uploaded, slug='product-1'
        )
        product_2 = Product.objects.create(
            title = 'Product 2', category=category, image=uploaded, slug='product-2'
        )
        response = self.client.get(reverse('shop:products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)