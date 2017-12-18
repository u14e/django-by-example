from decimal import Decimal
from django.conf import settings

from shop.models import Product


class Cart:
    """
    {
        'id1': {
            'price': 12.01,
            'quantity': 10,
            'product': product,
            'total_price': 120.1
        },
        'id2': {
            'price': 12.01,
            'quantity': 10,
            'product': product,
            'total_price': 120.1
        }
    }
    """

    def __init__(self, request):
        """
        初始化购物车
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 如果没有购物车，就在session里面保存空购物车对象(dict)
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        向购物车添加产品，或者更新产品数量
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        更新session
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True  # 告诉django，session改变，需要保存

    def remove(self, product):
        """
        从session中删除指定产品
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        从session中清空购物车
        :return:
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        """
        计算购物车中产品的总价格
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        迭代购物车中的所有产品id，从数据中获取产品对象
        :return:
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        计算购物车中产品总数量
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())
