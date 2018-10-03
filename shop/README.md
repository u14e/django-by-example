Django sessions
----

1. 确保 `settings.py` 的 `MIDDLEWARE` 里面包含 `SessionMiddleware` (默认是有的)

```python
MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ...
]
```

2. 在 `request.session` 里面操作session，操作方法和Python字典一样

```python
# 添加
request.session['foo'] = 'bar'

# 获取
request.session.get('foo')

# 删除
del request.session['foo']
```

> **注意**：当用户登录后，其从匿名用户切换成登录的某个用户，此时他们在登录前的匿名session将会丢失，并为登录用户创建了新的session。如果想要将匿名session加到登录用户的session，需要将匿名session复制到登录后的新session(即登录用户的session)

> 原文： When users log in to the site, their anonymous session is lost and a new
session is created for the authenticated users. If you store items in an
anonymous session that you need to keep after the user logs in, you will have
to copy the old session data into the new session.

3. 存储session数据的几种方式

- Database sessions(**默认**存入数据库中)
- File-based sessions(存入文件)
- Cached sessions(存入缓存,如Memcached、Redis, **有助于性能优化**)
- Cached database sessions(Session data is stored in a write-through cache and database. Reads-only use the database if the data is not already in the cache.)
- Cookie-based sessions(基于cookie, 存在浏览器中)

Context processors(上下文处理器)
----

`settings.py` 的 `TEMPLATES` 里面默认有以下四种上下文处理器, 所有模板都可以全局访问到他们

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

1. 创建一个请求上下文处理器:

```python
# 应用下 context_processors.py 编写处理器函数
# 接收request参数，返回Python字典
from .cart import Cart

def cart(request):
    return dict(cart=Cart(request))
```

2. `settings.py` 配置:

```python
TEMPLATES = [
    {
        # ...
        'OPTIONS': {
            'context_processors': [
                # ...
                'cart.context_processors.cart',
            ],
        },
    },
]
```

3. html中使用:

```html
{% cart... %}
```

创建订单
----

1. 用户填写订单表单
2. 创建Order实例，并为购物车里面的每项商品创建相关的OrderItem实例
3. 清空购物车
4. 发送下单成功邮件
5. 跳到支付页面，支付成功将order状态换成paid，并填入交易号

Celery
----

安装: `pipenv install celery[redis]`

1. 配置celery

```python
# app/celery.py

import os
from celery import Celery
# fix windows bug
# 参考链接：https://github.com/celery/celery/issues/4081
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

2. 导入celery

```python
# app/__init__.py
from .celery import app as celery_app
```

3. 应用下添加tasks.py

```python
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
```

4. views.py 里面调用任务

```python
from .tasks import order_created

def order_create(request):
    # ...
    order_created.delay(order.id)
    # ...
```

启动：

0. 确保安装redis并启动redis服务
1. 启动celery worker: `celery -A app worker -l info`
2. 启动项目：`python manage.py runserver`
3. 安装并启动flower监控工具: `pipenv shell flower` and `celery -A app flower` and 访问 `http://localhost:5555/`

支付
----

1. 创建sandbox账户：  https://www.braintreepayments.com/sandbox
2. 登录 https://sandbox.braintreegateway.com/login ：wh@字母+数字，获取 `Merchant ID`、`Public Key`、`Private Key`
3. 安装：`pipenv install braintree`
4. VISA 测试卡号: `4111 1111 1111 1111`, CVV: `123`, expiration date: `12/24`

