from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Category, Product


class HomeView(View):
    def get(self, request):
        categories = Category.objects.all()[:6]
        featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
        new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
        context = {
            'categories': categories,
            'featured_products': featured_products,
            'new_arrivals': new_arrivals,
        }
        return render(request, 'products/home.html', context)


class ShopView(View):
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        categories = Category.objects.all()

        category_slugs = request.GET.getlist('category')
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 10000)
        sizes = request.GET.getlist('size')
        sort = request.GET.get('sort', 'latest')

        if category_slugs:
            products = products.filter(category__slug__in=category_slugs)
        try:
            products = products.filter(price__gte=float(min_price), price__lte=float(max_price))
        except (ValueError, TypeError):
            pass
        if sizes:
            products = products.filter(sizes__size__in=sizes).distinct()

        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        else:
            products = products.order_by('-created_at')

        total_count = products.count()
        paginator = Paginator(products, 12)
        page_obj = paginator.get_page(request.GET.get('page'))

        context = {
            'products': page_obj,
            'categories': categories,
            'total_count': total_count,
            'selected_categories': category_slugs,
            'min_price': min_price,
            'max_price': max_price,
            'selected_sizes': sizes,
            'sort': sort,
            'all_sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
        }
        return render(request, 'products/shop.html', context)


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_active=True)
        related_products = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(id=product.id)[:4]
        context = {
            'product': product,
            'related_products': related_products,
            'sizes': product.sizes.all(),
            'images': product.images.all(),
        }
        return render(request, 'products/detail.html', context)
