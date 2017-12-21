
## fixtures：创建测试数据
```shell
# 从数据库中读取数据，并保存到subjects.json文件中
python manage.py dumpdata courses --indent=2 --output=courses/fixtures/subjects.json

# 从subjects.json中直接加载数据，保存到对应的数据库
# 默认从每个应用(如courses)里面的fixtures目录下寻找指定文件
python manage.py loaddata subjects.json

# 从数据库中读取数据，并以json格式打印到控制台
python manage.py dumpdata courses --indent=2

# 查看help信息
python manage.py dumpdata --help 
```

## model inheritance
- **Abstract models**: Useful when you want to put some common information
into several models. No database table is created for the abstract model.
- **Multi-table model inheritance**: Applicable when each model in the
hierarchy is considered a complete model by itself. A database table is
created for each model.
- **Proxy models**: Useful when you need to change the behavior of a model, for
example, including additional methods, changing the default manager, or
using different meta options. No database table is created for proxy models.

## Todo
- cache缓存，memcached的windows安装包下载网址访问不了

## build serializers
- **Serializer** : Provides serialization for normal Python class instances
- **ModelSerializer** : Provides serialization for model instances
- **HyperlinkedModelSerializer** : The same as  ModelSerializer , but
represents object relationships with links rather than primary keys

## REST Framework authentication backends
- **BasicAuthentication** : HTTP Basic Authentication. The user and password
are sent by the client in the  Authorization HTTP header encoded with
Base64. You can learn more about it at  https://en.wikipedia.org/wiki/
Basic_access_authentication .
- **TokenAuthentication** : Token-based authentication. A  Token model is used
to store user tokens. Users include the token in the  Authorization HTTP
header for authentication.
- **SessionAuthentication** : Uses Django's session backend for authentication.
This backend is useful to perform authenticated AJAX requests to the API
from your website's frontend.

## REST Framework  permission system
- **AllowAny** : Unrestricted access, regardless of if a user is authenticated or not.
- **IsAuthenticated** : Allows access to authenticated users only.
- **IsAuthenticatedOrReadOnly** : Complete access to authenticated users.
Anonymous users are only allowed to execute read methods such as GET,
HEAD, or OPTIONS.
- **DjangoModelPermissions** : Permissions tied to  django.contrib.auth . The
view requires a  queryset attribute. Only authenticated users with model
permissions assigned are granted permission.
- **DjangoObjectPermissions** : Django permissions on a per-object basis.