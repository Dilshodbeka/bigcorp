from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAdress

@login_required(login_url='account:login')
def shipping(request):
    try:
        shipping_adress = ShippingAdress.objects.get(user=request.user)
    except ShippingAdress.DoesNotExist:
        shipping_adress = None
    
    form = ShippingAddressForm(instance=shipping_adress)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_adress)
        if form.is_valid():
            shipping_adress = form.save(commit=False)
            shipping_adress.user= request.user
            shipping_adress.save()
            return redirect('account:dashboard')
    return render(request, 'payment/shipping.html', {'form': form})


def checkout(request):
    if request.user.is_authenticated:
        shipping_adress = get_object_or_404(ShippingAdress, user=request.user)
        if shipping_adress:
            return render(request, 'payment/checkout.html', {'shipping_adress': shipping_adress})
    return render(request, 'payment/checkout.html')

def complete_order(request):
    if request.POST.get('action') == 'payment':
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        country = request.POST.get('country')
        zip = request.POST.get('zip')

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address = ShippingAdress.objects.get_or_create(
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
    if request.user.is_authenticated:
        print(shipping_address, 'here sshipping_address****************************************')
        order = Order.objects.create(
            user=request.user, shipping_address=shipping_address, amount=total_price)

        for item in cart:
            OrderItem.objects.create(
                order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)
    else:
        order = Order.objects.create(
            shipping_address=shipping_address, amount=total_price)

        for item in cart:
            OrderItem.objects.create(
                order=order, product=item['product'], price=item['price'], quantity=item['qty'])

    return JsonResponse({'success': True})


def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment-success.html')


def payment_fail(request):
    return render(request, 'payment/payment-fail.html')