from decimal import Decimal
from django.http import JsonResponse

import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAdress

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


@login_required(login_url="account:login")
def shipping(request):
    try:
        shipping_adress = ShippingAdress.objects.get(user=request.user)
    except ShippingAdress.DoesNotExist:
        shipping_adress = None

    form = ShippingAddressForm(instance=shipping_adress)

    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipping_adress)
        if form.is_valid():
            shipping_adress = form.save(commit=False)
            shipping_adress.user = request.user
            shipping_adress.save()
            return redirect("account:dashboard")
    return render(request, "payment/shipping.html", {"form": form})


def checkout(request):
    if request.user.is_authenticated:
        shipping_adress = get_object_or_404(ShippingAdress, user=request.user)
        if shipping_adress:
            return render(
                request, "payment/checkout.html", {"shipping_adress": shipping_adress}
            )
    return render(request, "payment/checkout.html")


def complete_order(request):
      if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        country = request.POST.get('country')
        zip = request.POST.get('zip')

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAdress.objects.get_or_create(
            user=request.user,
            defaults={
                'name': name,
                'email': email,
                'street_address': street_address,
                'apartment_address': apartment_address,
                'country': country,
                'zip': zip
            }
        )

        match payment_type:
            case "stripe-payment":

                shipping_address, _ = ShippingAdress.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'name': name,
                        'email': email,
                        'street_address': street_address,
                        'apartment_address': apartment_address,
                        'country': country,
                        'zip': zip
                    }
                )
                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment-success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment-fail')),
                    'line_items': []
                }

                if request.user.is_authenticated:
                    order = Order.objects.create(
                        user=request.user, shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(
                            order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)

                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product']
                                },
                            },
                            'quantity': item['qty'],
                        })

                        session = stripe.checkout.Session.create(**session_data)
                        return redirect(session.url, code=303)
                else:
                    order = Order.objects.create(
                        shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(
                            order=order, product=item['product'], price=item['price'], quantity=item['qty'])



def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment-success.html')


def payment_fail(request):
    return render(request, "payment/payment-fail.html")
