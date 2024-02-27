from django import forms

from .models import ShippingAdress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        fields = ['full_name', 'email', 'street_adress', 'apartment_adress', 'country','zip_code']
        exclude = ['user']