
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
