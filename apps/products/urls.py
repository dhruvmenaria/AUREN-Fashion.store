from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
]
