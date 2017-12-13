from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

#  必须去掉，否则auth_views.password_change的函数执行时会报NoReverseMatch Reverse for 'xxx' not found
# app_name = 'account'
urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),

    # 登陆登出
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),

    # 修改密码
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),

    # 重置密码
    url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # 注册
    url(r'^register/$', views.register, name='register'),

    # 编辑用户资料
    url(r'^edit/$', views.edit, name='edit'),

    url(r'^$', views.dashboard, name='dashboard'),
]
