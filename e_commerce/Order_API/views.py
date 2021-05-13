from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Order_API.models import Cart, Order
from Shop_API.models import Product
from django.contrib import messages


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk = pk)
    order_item = Cart.objects.get_or_create(item = item, user = request.user, purchased = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item = item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item's quantity was updated")
            return redirect('Shop_API:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart")
            return redirect('Shop_API:home')
    else:
        order = Order(user = request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item was added to your cart")
        return redirect('Shop_API:home')

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user = request.user, purchased = False)
    orders = Order.objects.filter(user = request.user, ordered = False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'Order_API/cart.html', context = {'carts' : carts, 'order' : order})
    else:
        messages.warning(request, "You don't have any item in your cart")
        return redirect('Shop_API:home')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk = pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item = item).exists():
            order_item = Cart.objects.filter(item = item, user = request.user, purchased = False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "One item was removed from your cart")
            return redirect('Order_API:cart')
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('Shop_API:home')
    else:
        messages.info(request, 'Your cart is empty')
        return redirect('Shop_API:home')

@login_required
def increase_cart(request, pk):
        item = get_object_or_404(Product, pk = pk)
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item = item).exists():
                order_item = Cart.objects.filter(item = item, user = request.user, purchased = False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, "{} increased by one".format(item.name))
                    return redirect('Order_API:cart')
                else:
                    messages.info(request, "{} is not in your cart".format(item.name))
                    return redirect('Shop_API:home')
            else:
                messages.info(request, "You don't have any active order")
                return redirect('Shop_API:home')

@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk = pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item = item).exists():
            order_item = Cart.objects.filter(item = item, user = request.user, purchased = False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "{} decreased by one".format(item.name))
                return redirect('Order_API:cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "{} has been removed from your cart".format(item.name))
                return redirect('Order_API:cart')
        else:
            messages.info(request, " You don't have any active order")
            return redirect('Shop_API:home')
