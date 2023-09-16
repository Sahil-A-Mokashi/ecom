from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Order
from product.models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the item is already in the cart, increase the quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:view_cart')

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/view_cart.html', context)

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    order = Order.objects.create(user=request.user, cart=cart, total_price=total_price)

    # Clear the cart after placing the order
    cart.cartitem_set.all().delete()

    messages.success(request, 'Order placed successfully!')

    return redirect('cart:view_cart')