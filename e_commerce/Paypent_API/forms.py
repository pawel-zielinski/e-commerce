from django import forms
from Paypent_API.models import BillingAddress


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('address', 'zipcode', 'city', 'country')
