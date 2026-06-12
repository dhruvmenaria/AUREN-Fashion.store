from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:item_id>/', views.UpdateCartView.as_view(), name='update_cart'),
    path('remove/<int:item_id>/', views.RemoveCartView.as_view(), name='remove_cart'),
]
