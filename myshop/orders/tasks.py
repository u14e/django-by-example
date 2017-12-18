from celery import task
from django.core.mail import send_mail
from django.conf import settings

from .models import Order


@task
def order_created(order_id):
    """
    celery任务：当订单成功时，发送邮件通知
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order number: {}'.format(order.id)
    message = 'Dear {}, \n\nYou have successfully placed an order.' \
              'Your order id is {}'.format(order.username, order.id)
    mail_sent = send_mail(subject, message,
                          settings.DEFAULT_FROM_EMAIL,
                          [order.email])
    return mail_sent
