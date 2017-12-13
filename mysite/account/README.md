## 注销时，重定向到admin的注销页面
在头部点击logout时，页面重定向到admin的log out页面，这里需要在`settings.py`的`INSTALLED_APPS`里面，把`account`放在` django.contrib.admin`前面，参考链接：[django logout redirects me to administration page
](https://stackoverflow.com/questions/15467831/django-logout-redirects-me-to-administration-page#)

## 给命名空间account后，访问`/account/password-change/`出现`NoReverseMatch at /account/password-change/`错误
这里查看`django.contrib.auth.views.password_change`的源码，发现在执行到`reverse('password_change_done')`时，报出上面的错误，改为`reverse('account:password_change_done')`就可以了，具体原因不知道，但是在修改django源码显然不是明智之举，所以不要account的命名空间了。

```python 
# django.contrib.auth.views.py的password_change函数节选
if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
```
```python
# 去掉app_name命名空间
# app_name = 'account'
urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    # ...
]
```

## 使用python-social-auth进行社交认证登陆
> http://python-social-auth.readthedocs.io/en/latest/configuration/django.html
1. pip install social-auth-app-django
2. `settings.py`里面配置
```python
INSTALLED_APPS = (
    ...
    'social_django',
    ...
)
```
3. 执行`python manage.py migrate`
4. 添加相关社交平台的认证后台
```python
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOpenId',
    ...
    'django.contrib.auth.backends.ModelBackend',
)
```
5. 项目的`urls.py`里面添加`url(r'^socia-auth/', include('social_django.urls'), name='social')`
6. `ALLOWED_HOSTS`添加'ALLOWED_HOSTS = ['localhost', '127.0.0.1']'，经过测试这两个现在都可以了，所以不需要改host，记得在谷歌凭证那里的url添加对应的域名，
我这里也把两个都添加了，`http://127.0.0.1:8000/social-auth/complete/google-oauth2/`和`http://localhost:8000/social-auth/complete/google-oauth2/`
7. 链接`{% url "social:begin" "google-oauth2" %}`
