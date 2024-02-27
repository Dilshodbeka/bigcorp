from django.contrib import admin

from .models import Order, ShippingAdress, OrderItem

admin.site.register(Order)
admin.site.register(ShippingAdress)
admin.site.register(OrderItem)