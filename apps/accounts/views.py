from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order
from .forms import RegisterForm, LoginForm


def merge_guest_cart(request, user):
    """Merge guest session cart into the user's cart on login."""
    session_key = request.session.session_key
    if not session_key:
        return
    guest_cart = Cart.objects.filter(session_key=session_key, user=None).first()
    if not guest_cart:
        return
    user_cart, _ = Cart.objects.get_or_create(user=user)
    for item in guest_cart.items.all():
        existing = CartItem.objects.filter(cart=user_cart, product=item.product, size=item.size).first()
        if existing:
            existing.quantity += item.quantity
            existing.save()
        else:
            item.cart = user_cart
            item.save()
    guest_cart.delete()


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:home')
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            merge_guest_cart(request, user)
            login(request, user)
            messages.success(request, f'Welcome to NAINA, {user.first_name}!')
            return redirect('products:home')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:home')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            merge_guest_cart(request, user)
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.email}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('products:home')


class ProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'accounts/profile.html', {'orders': orders})
