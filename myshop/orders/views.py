from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


# from .tasks import order_created


def order_create(req):
    cart = Cart(req)
    if req.method == 'POST':
        form = OrderCreateForm(req.POST)
        if form.is_valid():
            # 保存订单
            order = form.save(commit=False)
            if cart.coupon:
                # 有优惠券的情况下
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            # 保存订单清单
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # 清空购物车
            # order_created.delay(order.id)  # 发送celery异步邮件
            # return render(req, 'orders/order/created.html', {'order': order})
            req.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(req, 'orders/order/create.html', {'cart': cart,
                                                    'form': form})


@staff_member_required
def admin_order_detail(req, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(req, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(req, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' \
                                      'order_{}.pdf'.format(order.id)
    # weasyprint.HTML(string=html).write_pdf(response,
    #                                        stylesheets=[weasyprint.CSS(
    #                                            settings.STATIC_ROOT + 'css/pdf.css'
    #                                        )])
    return response
