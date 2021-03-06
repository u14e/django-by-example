from decimal import Decimal
from django.conf import settings

from shop.models import Product
from coupons.models import Coupon


class Cart(object):
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

        self.coupon_id = self.session.get('coupon_id')

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """
        优惠金额
        """
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        """
        优惠之后的总价
        """
        return self.get_total_price() - self.get_discount()

    def add(self, product, quantity=1, update_quantity=False):
        """
        往购物车添加产品或者更新产品数量
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = dict(quantity=0,
                                         price=str(product.price))
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        更新session
        """
        self.session.modified = True

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
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        迭代购物车中的所有产品id，从数据中获取产品对象
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        计算购物车中产品总数量
        """
        return sum(item['quantity'] for item in self.cart.values())