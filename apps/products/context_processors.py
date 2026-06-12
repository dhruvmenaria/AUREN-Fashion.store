from .models import Category


def products_context(request):
    try:
        categories = Category.objects.all()[:5]
    except Exception:
        categories = []
    return {
        'nav_categories': categories
    }
