from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. 创建订单
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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

            request.session['order_id'] = order.id
            del request.session['coupon_id']
            # 重定向到支付页面
            return redirect(reverse('payment:process'))
            # data = dict(
            #     order=order
            # )
            #
            # return render(request,
            #               'orders/order/created.html',
            #               data)

    else:
        form = OrderCreateForm()

    data = dict(
        cart=cart,
        form=form
    )

    return render(request,
                  'orders/order/create.html',
                  data)


@staff_member_required
def admin_order_detail(request, order_id):
    """
    admin管理后台的订单详情页面
    """
    order = get_object_or_404(Order, id=order_id)
    data = dict(
        order=order
    )
    return render(request,
                  'admin/orders/order/detail.html',
                  data)


# @staff_member_required
# def admin_order_pdf(request, order_id):
#     """
#     admin管理后台导出订单pdf文件
#     """
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html', {'order': order})
#     response = HttpResponse(content_type='application/pdf; charset=utf-8')
#     response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
#     weasyprint\
#         .HTML(string=html)\
#         .write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
#     return response