from django.test import TestCase, RequestFactory, Client

import json

from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from shop.models import Category, ProductProxy

from .views import cart_view, cart_add, cart_delete, cart_update



class CartViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get[reverse('cart:cart-view')]
        self.middleware = SessionMiddleware(self.client)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    
    def test_cart_view(self):
        request = self.factory
        response = cart_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart-view.html')