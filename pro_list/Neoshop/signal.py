from django.contrib.auth.signals import user_logged_in
from django.shortcuts import render,redirect,get_object_or_404
from .models import products,Cart,SubCategory,CartItem

def transfer_session_cart_to_user(sender, user, request, **kwargs):
    session_cart = request.session.get('cart', {})
    cart, created = Cart.objects.get_or_create(user=user)
    
    for product_id, item in session_cart.items():
        product = get_object_or_404(products, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += item['quantity']
        else:
            cart_item.quantity = item['quantity']
        cart_item.save()
    
    request.session['cart'] = {}
    
user_logged_in.connect(transfer_session_cart_to_user)