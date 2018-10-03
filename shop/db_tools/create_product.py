import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

if __name__ == '__main__':
    import django
    django.setup()

    from shop.models import Category, Product
    from shop.recommender import Recommender

    tea = Category.objects.get(slug='tea')

    black_tea = Product.objects.create(category=tea, name='Black_tea', slug='black_tea', price=11, stock=4)
    red_tea = Product.objects.create(category=tea, name='Red_tea', slug='red_tea', price=12, stock=4)
    green_tea = Product.objects.create(category=tea, name='Green_tea', slug='green_tea', price=13, stock=4)
    tea_powder = Product.objects.create(category=tea, name='Tea_powder', slug='tea_powder', price=14, stock=4)

    r = Recommender()
    r.products_bought([black_tea, red_tea])
    r.products_bought([black_tea, green_tea])
    r.products_bought([red_tea, black_tea, tea_powder])
    r.products_bought([green_tea, tea_powder])
    r.products_bought([black_tea, tea_powder])
    r.products_bought([red_tea, green_tea])
