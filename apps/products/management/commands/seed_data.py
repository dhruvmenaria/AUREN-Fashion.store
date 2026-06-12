from django.core.management.base import BaseCommand
from apps.products.models import Category, Product, ProductImage, ProductSize
import random


class Command(BaseCommand):
    help = 'Seed the database with NAINA products that use local catalog images'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        ProductImage.objects.all().delete()
        ProductSize.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_data = [
            {'name': 'Tops', 'slug': 'tops'},
            {'name': 'Bottoms', 'slug': 'bottoms'},
            {'name': 'Dresses', 'slug': 'dresses'},
            {'name': 'Outerwear', 'slug': 'outerwear'},
            {'name': 'Accessories', 'slug': 'accessories'},
        ]
        categories = {
            data['name']: Category.objects.create(name=data['name'], slug=data['slug'])
            for data in categories_data
        }

        products_data = [
            {
                'name': "Men's Gold Gemstone Bracelet",
                'category': 'Accessories',
                'price': 1299,
                'sale_price': None,
                'featured': True,
                'description': 'A gold-tone statement bracelet finished with colored gemstone detailing for a sharp dressed-up accent.',
                'image': '/static/img/products/gold-gemstone-bracelet.jpg',
            },
            {
                'name': 'Black Luxe Accessories Set',
                'category': 'Accessories',
                'price': 2499,
                'sale_price': 2199,
                'featured': True,
                'description': 'A polished black-and-gold accessories edit with heels, bag, jewelry, watch, lipstick, and fragrance styling.',
                'image': '/static/img/products/black-luxe-accessories.jpg',
            },
            {
                'name': 'Y2K Varsity Streetwear Set',
                'category': 'Tops',
                'price': 2799,
                'sale_price': None,
                'featured': True,
                'description': 'A relaxed Y2K-inspired varsity pullover look styled with wide black pants and red sneakers.',
                'image': '/static/img/products/y2k-varsity-set.jpg',
            },
            {
                'name': 'Black Long Coat Outfit',
                'category': 'Outerwear',
                'price': 3999,
                'sale_price': None,
                'featured': True,
                'description': 'A monochrome long coat look with a fitted black dress, knee boots, and a sleek shoulder bag.',
                'image': '/static/img/products/black-long-coat-outfit.jpg',
            },
            {
                'name': 'Casual Stripe Shirt Fit',
                'category': 'Tops',
                'price': 1899,
                'sale_price': 1599,
                'featured': True,
                'description': 'A relaxed blue striped shirt layered over a white crop top with wide cream trousers and a woven bag.',
                'image': '/static/img/products/casual-stripe-shirt-fit.jpg',
            },
            {
                'name': 'Ribbed Polo Shirt Edit',
                'category': 'Tops',
                'price': 1699,
                'sale_price': None,
                'featured': False,
                'description': 'A smart casual ribbed polo edit with neutral, navy, cream, and brown styling references.',
                'image': '/static/img/products/ribbed-polo-shirts.jpg',
            },
            {
                'name': 'Old Money Leather Jacket',
                'category': 'Outerwear',
                'price': 3499,
                'sale_price': None,
                'featured': True,
                'description': 'A cropped black leather jacket styled with denim for an old-money winter streetwear finish.',
                'image': '/static/img/products/old-money-leather-jacket.jpg',
            },
            {
                'name': 'Leather Jacket Tie Fit',
                'category': 'Outerwear',
                'price': 3799,
                'sale_price': 3299,
                'featured': False,
                'description': 'A structured black leather jacket layered with a white shirt, black tie, belt, and tailored grey trousers.',
                'image': '/static/img/products/leather-jacket-tie-fit.jpg',
            },
        ]

        sizes_list = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

        self.stdout.write('Creating products...')
        for data in products_data:
            product = Product.objects.create(
                name=data['name'],
                category=categories[data['category']],
                description=data['description'],
                price=data['price'],
                sale_price=data['sale_price'],
                is_featured=data['featured'],
                is_active=True,
            )
            ProductImage.objects.create(
                product=product,
                image_url=data['image'],
                is_primary=True,
            )
            for size in sizes_list:
                ProductSize.objects.create(
                    product=product,
                    size=size,
                    stock=random.randint(5, 30),
                )
            self.stdout.write(f'  Created: {product.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully seeded {len(products_data)} products across {len(categories_data)} categories!'
        ))
