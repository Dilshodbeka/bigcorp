from . import views
from django.urls import path

app_name = 'payment'

urlpatterns = [
    path('payment-success', views.payment_success, name='payment-success'),
    path('payment-fail', views.payment_fail, name='payment-fail'),
    path('shipping/', views.shipping, name='shipping'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete-order', views.complete_order, name='complete-order'),
]