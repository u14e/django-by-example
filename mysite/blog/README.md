## 邮件
QQ邮箱不管25端口，还是465/587开启SSL都没效，后面改用网易163的有效，参考链接[django发送邮件](http://www.jianshu.com/p/6ab798cd4864)

## solr
1. 执行`python manage.py build_solr_schema`出现`TypeError context must be a dict rather than Context`错误，
这里可以参看stackoverflow [TypeError: context must be a dict rather than Context](https://stackoverflow.com/questions/45739518/typeerror-context-must-be-a-dict-rather-than-context)。
在`site-packages/haystack/management/commands/build_solr_schema.py`文件的第45行，将return语句改成普通的字典就可以了。

如图：
```python
return {
    'content_field_name': content_field_name,
    'fields': fields,
    'default_operator': constants.DEFAULT_OPERATOR,
    'ID': constants.ID,
    'DJANGO_CT': constants.DJANGO_CT,
    'DJANGO_ID': constants.DJANGO_ID,
}

```

2. 执行search搜索时，必须`java -jar start.jar`开启solr搜索服务，否则会搜不到东西
3. 关于搜索所用的模块版本，solr使用4.10.4，django-haystack和pysolr最新就可以了