from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Paypent_API.models import BillingAddress
from Paypent_API.forms import BillingForm
from Order_API.models import Order, Cart


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user = request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance = saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance = saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance = saved_address)
            messages.success(request, "Everything seems to be OK. Lets continue!")

    order_qs = Order.objects.filter(user = request.user, ordered = False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()

    return render(request, 'Payment_API/checkout.html', context = {'form' : form, 'order_items' : order_items, 'order_total' : order_total})
