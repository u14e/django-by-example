1. 开始Django项目
----

```bash
mkdir blog(cd blog) # 创建目录
pipenv install  # 安装虚拟环境
pipenv shell  # 激活虚拟环境
pipenv install django==2.1  # 安装django
django-admin startproject app . # 创建项目
python manage.py migrate  # 迁徙
python manage.py runserver  # 启动服务
# 扩展 python manage.py runserver 127.0.0.1:8081 --settings=app.settings
python manage.py createsuperuser  # 创建超级用户
```

2. 开发应用
----

```bash
# 1. 创建app应用
python manage.py startapp blog
# 2. 编写model
# 3. settings.py激活应用
# 4. 创建迁徙仓库
python manage.py makemigrations blog
# 5. 运行迁徙脚本
python manage.py migrate
# 6. 注册后台
# 7. 编写views
# 8. 注册urls
# 9. 编写template渲染函数
```

`settings`配置
----

```bash
TIME_ZONE = 'Asia/Shanghai'
```


ORM
----

```bash
# get
user = User.objects.get(username='admin') # 可能的错误 DoesNotExist or MultipleObjectsReturned

# create
## 两步
post = Post(title='Game', slug='game', body='This is a game', author=user)
post.save()
## 一步
Post.objects.create(title='Game', slug='game', body='This is a game', author=user)

# update
post.title = 'New game'
post.save()

# retrieve
all_posts = Post.objects.all()

# filter
Post.objects.filter(publish__year=2015, author__username='admin')
Post.objects.filter(publish__year=2015).filter(author__username='admin')

# exclude
Post.objects.filter(publish__year=2015).exclude(title__startswith='Why')

# order_by
Post.objects.order_by('title')

# delete
post = Post.objects.get(id=1)
post.delete()
```

> `objects`是默认的`manager`
> 查询结果是`QuerySet`

`QuerySet`执行的时机：
- 第一次迭代
- 使用切片(`Post.objects.all()[:3]`)
- 序列化(`pickle`)或者缓存(`cache`)
- 调用`repr()`或`len()`
- 调用`list()`
- 测试时`bool()`、`or`、`and`、`if`

创建manager的两种方法：
- 添加额外的manager方法: `Post.objects.my_manager()`
- 修改默认的manager: `Post.my_manager.all()`

表单
----

```python
# forms.py定义表单 EmailPostForm
if request.method == 'POST':
    form = EmailPostForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    else:
        form.errors
else:
    form = EmailPostForm()
```

发邮件
----

```bash
# settings.py
# 1. 控制台本地查看邮件发送信息
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 2. gmail邮件服务
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '账户'
EMAIL_HOST_PASSWORD = '密码'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

模板标签(template tags)
----

- `simple_tag`: 返回字符串
- `inclusion_tag`: 返回一个渲染后的模板

模板过滤器(template filters)
----

类似于模板标签，也是用register注册，使用的时候是 `{{ variable|filter1|filter2 }}`
