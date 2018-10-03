from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import braintree
# import weasyprint
from io import BytesIO

from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()

            # # 发送发票email
            # subject = 'My Shop - Invoice no. {}'.format(order.id)
            # message = 'Please, find attached the invoice for your recent purchase'
            # email = EmailMessage(subject,
            #                      message,
            #                      'admin@shop.com',
            #                      [order.email])
            # html = render_to_string('orders/order/pdf.html', {'order': order})
            # out = BytesIO()
            # weasyprint\
            #     .HTML(string=html)\
            #     .write_pdf(out, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
            # # 添加附件
            # email.attach('order_{}.pdf'.format(order.id),
            #              out.getvalue(),
            #              'application/pdf')
            # # 发送email
            # email.send()

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = braintree.ClientToken.generate()
        data = dict(
            order=order,
            client_token=client_token
        )
        return render(request,
                      'payment/process.html',
                      data)


def payment_done(request):
    return render(request,
                  'payment/done.html')


def payment_canceled(request):
    return render(request,
                  'payment/canceled.html')
