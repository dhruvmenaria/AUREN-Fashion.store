from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from apps.cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


class CheckoutView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_cart(self, request):
        return Cart.objects.filter(user=request.user).first()

    def get(self, request):
        cart = self.get_cart(request)
        if not cart or cart.items.count() == 0:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart:cart')
        form = CheckoutForm(initial={
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
        })
        subtotal = cart.total
        delivery = 0 if subtotal >= 999 else 99
        return render(request, 'orders/checkout.html', {
            'form': form, 'cart': cart,
            'subtotal': subtotal, 'delivery': delivery, 'total': subtotal + delivery
        })

    def post(self, request):
        cart = self.get_cart(request)
        if not cart or cart.items.count() == 0:
            return redirect('cart:cart')
        form = CheckoutForm(request.POST)
        subtotal = cart.total
        delivery = 0 if subtotal >= 999 else 99
        total = subtotal + delivery
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
                order_notes=form.cleaned_data.get('order_notes', ''),
                total_amount=total,
            )
            for item in cart.items.all():
                price = item.product.sale_price if item.product.sale_price else item.product.price
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    size=item.size,
                    quantity=item.quantity,
                    price=price,
                )
            cart.items.all().delete()
            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('orders:confirmation', order_number=order.order_number)
        return render(request, 'orders/checkout.html', {
            'form': form, 'cart': cart,
            'subtotal': subtotal, 'delivery': delivery, 'total': total
        })


class OrderConfirmationView(View):
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        return render(request, 'orders/confirmation.html', {'order': order})
