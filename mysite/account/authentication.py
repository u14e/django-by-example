from django.contrib.auth.models import User
from django.contrib import messages


class EmailAuthBackend(object):
    """
    通过email认证登陆（注：email字段必须唯一，否则会报MultipleObjectsReturned）
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
