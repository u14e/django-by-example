## 使用[uuslug](https://github.com/un33k/django-uuslug)`来替代django自带的slugify`
## redis
- 使用redis时，在执行redis操作时，一直没响应，发现是redis服务挂了，需要重启下
- redis安装时，最好不要安装到系统盘，不然每次重启服务，redis因为没有权限，没有保存上次的数据
## 分页之前要排序
`images/views.py`里面的image_list在分页的时候报出警告
```python
UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'images.models.Image'> QuerySet.
  paginator = Paginator(images, 8)
```
所以在分页之前需要把序列有序化，可以在model里面的Meta添加ordering，也可以在views里面的为query_set添加属性order_by，如下
```python
images = Image.objects.all().order_by('created')
paginator = Paginator(images, 8)
```
