from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from ..models import Post


# simple_tag : Processes the data and returns a string
@register.simple_tag
def total_posts():
    return Post.published.count()


# inclusion_tag : Processes the data and returns a rendered template
@register.inclusion_tag('blog/post/lastest_posts.html')
def show_lastest_posts(count=5):
    """
    显示最新的几篇文章
    :param count: 限定文章数
    :return: 用于模板的上下文
    """
    lastest_posts = Post.published.order_by('-publish')[:count]
    return {'lastest_posts': lastest_posts}


# assignment_tag : Processes the data and sets a variable in the context
@register.assignment_tag
def get_most_commented_posts(count=5):
    """
    返回数据作为上下文供模板使用（在模板中调用assignment_tag，将结果赋值给变量共模板使用）
    :param count: 限定文章数
    :return: 数据
    """
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


"""
1. 新建blog_tags.py
2. 编写模板标签total_posts
3. 在模板base.html中{% load blog_tags %}
4. 在模板中使用{% total_posts %}
重启服务
"""
