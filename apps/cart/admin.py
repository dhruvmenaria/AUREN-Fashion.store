from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'get_item_count', 'created_at']
    inlines = [CartItemInline]

    def get_item_count(self, obj):
        return obj.item_count
    get_item_count.short_description = 'Items'
