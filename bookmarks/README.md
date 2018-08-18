Django用户认证
----

> 在`django.contrib.auth.views`

登录登出
----

- `LoginView`: 登录
- `LogoutView`: 登出

修改密码
----

- `PasswordChangeView`: 修改密码
- `PasswordChangeDoneView`: 密码修改成功后

重置密码
----

- `PasswordResetView`: 重置密码(填写邮件，生成一个带有token的一次性的link发送给用户邮件)
- `PasswordResetDoneView`: 告诉用户重置邮件已经发出
- `PasswordResetConfirmView`: 输入新密码
- `PasswordResetCompleteView`: 密码重置成功

`User Model`
----
- 直接获取Model:
    ```python
    from django.contrib.auth.models import User
    class UserRegistrationForm(forms.ModelForm):
        password = forms.CharField(label='密码', widget=forms.PasswordInput)
        password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
    ```
- 使用`settings.AUTH_USER_MODEL`(通过`get_user_model()`获取):
    ```python
    from django.conf import settings

    class Profile(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE)   # 用户user删除时，此profile也相应删除
    ```

图片上传
----
- 安装`Pillow`
- `settings.py`
    ```python
    MEDIA_URL = '/media/'   # 基本url
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')   # 本地路径
    ```
- `app -> urls.py`:
    ```python
    from django.conf import settings
    from django.conf.urls.static import static

    # 生产环境下不要使用Django发送多媒体文件
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
    ```

- `models.py`编写upload字段:
    ```python
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    ```

`messages`消息
----
用于显示一次性的消息，即用户进行下一个请求时显示此消息。默认存在cookie（或者session storage）

```python
from django.contrib import messages
messages.error(request, 'Somthing went wrong')
```

分类：
- `success()`
- `info()`
- `warning()`
- `error()`
- `debug()`：生产环境不会显示

自定义用户认证
----
- `authenticate()`: 通过可选的参数检索用户，返回匹配的`user`，否则返回`None`
- `get_user()`: 通过用户`ID`检索用户，返回匹配的`user`，否则返回`None`

```python
from django.contrib.auth.models import User

class EmailAuthBackend(object):
    """
    使用email进行登录认证
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNoeExists:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

`settings.py`

> 认证顺序从上到下，返回第一个匹配的user

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',    # 默认的
    'account.authentication.EmailAuthBackend'   # 自定义的
]
```