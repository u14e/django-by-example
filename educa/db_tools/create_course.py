import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

if __name__ == '__main__':
    import django
    django.setup()

    from django.contrib.auth import get_user_model
    from courses.models import Subject, Course, Module

    User = get_user_model()

    user = User.objects.last()
    subject = Subject.objects.get(slug='music')

    c1 = Course.objects.create(subject=subject,
                               owner=user,
                               title='Course 1',
                               slug='course1')
    m1 = Module.objects.create(course=c1, title='Module 1')
    m2 = Module.objects.create(course=c1, title='Module 2')
    m3 = Module.objects.create(course=c1, title='Module 3', order=5)
    m4 = Module.objects.create(course=c1, title='Module 4')

    c2 = Course.objects.create(subject=subject,
                               owner=user,
                               title='Course 2',
                               slug='course2')
    m5 = Module.objects.create(course=c2, title='Module 1')