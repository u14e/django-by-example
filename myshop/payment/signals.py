from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
# import weasyprint

from orders.models import Order


# receiver接收器函数
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()
        # 生成pdf邮件
        subject = 'My Shop - Invoice no. {}'.format(order.id)
        message = 'Please, find attached the invoice for your recent purchase'
        email = EmailMessage(subject, message,
                             settings.DEFAULT_FROM_EMAIL,
                             [order.email])
        # 生成pdf
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        # weasyprint.HTML(string=html).write_pdf(out, stylesheets=[weasyprint.CSS(
        #     settings.STATIC_ROOT + 'css/pdf.css'
        # )])
        # 为email加pdf附件
        email.attach('order_{}'.format(order.id), out.getvalue(), 'application/pdf')
        # 发送邮件
        email.send()


valid_ipn_received.connect(payment_notification)
