from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from orders.models import Order


def payment_process(req):
    order_id = req.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = req.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:cancel')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(req, 'payment/process.html', {'order': order,
                                                'form': form})


@csrf_exempt  # 避免django需要处理csrf token
def payment_done(req):
    return render(req, 'payment/done.html')


@csrf_exempt  # 避免django需要处理csrf token
def payment_cancel(req):
    return render(req, 'payment/cancel.html')
