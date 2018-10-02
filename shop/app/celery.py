import os
from celery import Celery

# fix windows bug
# 参考链接：https://github.com/celery/celery/issues/4081
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('shop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
