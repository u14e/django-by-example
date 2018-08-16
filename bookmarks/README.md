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