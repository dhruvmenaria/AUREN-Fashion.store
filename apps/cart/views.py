from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from apps.products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


class CartView(View):
    def get(self, request):
        cart = None
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key, user=None).first()
        return render(request, 'cart/cart.html', {'cart': cart})


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        size = request.POST.get('size', 'M')
        quantity = int(request.POST.get('quantity', 1))
        cart = get_or_create_cart(request)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        messages.success(request, f'"{product.name}" added to your cart.')
        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('cart:cart')


class UpdateCartView(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
        return redirect('cart:cart')


class RemoveCartView(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        product_name = item.product.name
        item.delete()
        messages.success(request, f'"{product_name}" removed from cart.')
        return redirect('cart:cart')
