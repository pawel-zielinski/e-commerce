from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from Paypent_API.models import BillingAddress
from Paypent_API.forms import BillingForm
from Order_API.models import Order, Cart

# Payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket


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
            if saved_address.is_fully_filled():
                messages.success(request, "Everything seems to be OK. Lets continue!")
            else:
                messages.success(request, "Please, fill up all the information to make a payment")

    order_qs = Order.objects.filter(user = request.user, ordered = False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()

    return render(request, 'Payment_API/checkout.html', context = {
        'form' : form,
        'order_items' : order_items,
        'order_total' : order_total,
        'saved_address' : saved_address,
    })

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user = request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, "Please complete shipping address")
        return redirect('Paypent_API:checkout')

    if not request.user.profile.is_filled():
        messages.info(request, "Please complete your profile details")
        return redirect('Login_API:profile')

    mypayment = SSLCSession(
        sslc_is_sandbox = True,
        sslc_store_id = 'easyl5ef49b890c659',
        sslc_store_pass = 'easyl5ef49b890c659@ssl'
    )

    status_url = request.build_absolute_uri(reverse('Paypent_API:complete'))
    mypayment.set_urls(
        success_url = status_url,
        fail_url = status_url,
        cancel_url = status_url,
        ipn_url = status_url
    )

    order_qs = Order.objects.filter(user = request.user, ordered = False)
    order_items = order_qs[0].orderitems.all()
    order_item_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()

    mypayment.set_product_integration(
        total_amount = Decimal(order_total),
        currency = 'BDT',
        product_category = 'Mixed',
        product_name = order_items,
        num_of_item = order_item_count,
        shipping_method = 'Courier',
        product_profile = 'None'
    )

    current_user = request.user

    mypayment.set_customer_info(
        name = current_user.profile.full_name,
        email = current_user.email,
        address1 = current_user.profile.address,
        address2 = current_user.profile.address,
        city = current_user.profile.city,
        postcode = current_user.profile.zipcode,
        country = current_user.profile.country,
        phone = current_user.profile.phone
    )

    mypayment.set_shipping_info(
        shipping_to = current_user.profile.full_name,
        address = saved_address.address,
        city = saved_address.city,
        postcode = saved_address.zipcode,
        country = saved_address.country
    )

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, "Your payment was completed successfully!")
            return HttpResponseRedirect(reverse('Paypent_API:purchase', kwargs = {'val_id' : val_id, 'tran_id' : tran_id}))
        elif status == 'FAILED':
            messages.warning(request, "Your payment was declined. Please try again!")

    return render(request, 'Payment_API/complete.html', context = {})

@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    order = order_qs[0]
    order.ordered = True
    order.order_id = tran_id
    order.payment_id = val_id
    order.save()

    cart_items = Cart.objects.filter(user = request.user, purchased = False)
    for item in cart_items:
        item.purchased = True
        item.save()

    return HttpResponseRedirect(reverse('Shop_API:home'))
