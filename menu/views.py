from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, MenuItem, Order, OrderItem
from booking.models import Booking
from django.db import transaction
from django.contrib.auth.decorators import login_required

def menu_list(request):
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'menu/menu_list.html', {'categories': categories})

def add_to_cart(request,item_id):
    cart = request.session.get('cart',{})

    item_id_str = str(item_id)

    if item_id_str in cart:
        cart[item_id_str] = cart[item_id_str] + 1
    else:
        cart[item_id_str] = 1

    request.session['cart'] = cart
    return redirect('menu:menu_list')

def cart_detail(request):
    cart = request.session.get('cart',{})
    cart_items = []
    total_price = 0

    for item_id , quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        total_item_price = item.price * quantity
        total_price += total_item_price
        cart_items.append({
            'item' : item,
            'quantity' : quantity,
            'total_item_price' : total_item_price,
        })
    return render(request, 'menu/cart.html', {
        'cart_items': cart_items,
        'total_price' : total_price,
    })

@login_required
def checkout(request):
    cart = request.session.get('cart',{})
    if not cart:
        return redirect('menu:menu_list')
    last_booking = Booking.objects.filter(user=request.user).last()
    if not last_booking:
        return redirect('booking:table_list')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            table=last_booking.table,
        )

        total = 0
        for item_id, quantity in cart.items():
            product = MenuItem.objects.get(id=item_id)
            price = product.price * quantity
            total += price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )
        order.total_price = total
        order.save()
        request.session['cart'] = {}\

    return render(request, 'menu/success.html', {'order': order})