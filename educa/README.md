课程目录的数据结构

```
Subject 1
  Course 1
    Module 1
      Content 1 (image)
      Content 2 (text)
    Module 2
      Content 3 (text)
      Content 4 (file)
      Content 5 (video)
```

`fixtures`: 在数据库和本地文件之间加载或者转存数据(load data and dump data)
----

```bash
# 从数据库输出到控制台(标准输出,standard output)，默认是json格式(--output 指明输出的文件)
python manage.py dumpdata courses --indent=2
# 转存到文件
python manage.py dumpdata courses --indent=2 --output=courses/fixtures/subjects.json

# 从本地文件加载数据到数据库(默认从每个应用下面的fixtures文件夹下寻找文件,也可以通过FIXTURE_DIRS添加其他的目录)
python manage.py loaddata subjects.json
```

`model inheritance`: model继承
----

- **Abstract models**: Useful when you want to put some common information into several models. No database table is created for the abstract model.
- **Multi-table model inheritance**: Applicable when each model in the hierarchy is considered a complete model by itself. A database table is created for each model.
- **Proxy models**:  Useful when you need to change the behavior of a model, for example, including additional methods, changing the default manager, or using different meta options. No database table is created for proxy models.

```python
# Abstract models
class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Text(BaseContent):
    body = models.TextField()

# Multi-table model inheritance
class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class Text(BaseContent):
    body = models.TextField()
  
# Proxy models
# 新增一个排序和一个created_delta方法
from django.utils import timezone

class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class OrderedContent(BaseContent):
    class Meta:
        proxy = True
        ordering = ['created']

    def created_delta(self):
        return timezone.now() - self.created
```
