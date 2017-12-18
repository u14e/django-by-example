from django.shortcuts import render

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(req):
    cart = Cart(req)
    if req.method == 'POST':
        form = OrderCreateForm(req.POST)
        if form.is_valid():
            # 保存订单
            order = form.save()
            # 保存订单清单
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # 清空购物车
            order_created.delay(order.id)  # 发送celery异步邮件
        return render(req, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(req, 'orders/order/create.html', {'cart': cart,
                                                    'form': form})
