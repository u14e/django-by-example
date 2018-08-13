from django.shortcuts import render, get_object_or_404
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

from .models import Post

def post_list(request):
    object_list = Post.published.all()

    paginator = Paginator(object_list, 3)   # 每页3篇
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果page超出总页数，返回最后一页
        posts = paginator.page(paginator.num_pages)

    data = dict(
        posts=posts,
        page=page,
    )

    return render(request,
                  'blog/post/list.html',
                  data)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    data = dict(
        post=post
    )

    return render(request,
                  'blog/post/detail.html',
                  data)
