from celery import task
from django.core.mail import send_mail

from .models import Order

@task
def order_created(order_id):
    """
    当订单成功创建后，发送一封邮件通知
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order number: {}'.format(order.id)
    message = 'Dear {}, \n\nYou have successfully placed an order.' \
              'Your order id is {}'.format(order.username, order.id)
    mail_sent = send_mail(subject, message,
                          'admin@shop.com',
                          [order.email])
    return mail_sent