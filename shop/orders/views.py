from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. 创建订单
            order = form.save()
            # 2. 创建订单清单
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 3. 清空购物车
            cart.clear()
            # 4. 发送异步邮件
            order_created.delay(order.id)

            data = dict(
                order=order
            )
            return render(request,
                          'orders/order/created.html',
                          data)

    else:
        form = OrderCreateForm()

    data = dict(
        cart=cart,
        form=form
    )

    return render(request,
                  'orders/order/create.html',
                  data)