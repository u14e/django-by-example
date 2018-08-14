from django.shortcuts import render, get_object_or_404
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.core.mail import send_mail
from django.db.models import Count

from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

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
        tag=tag
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

    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 创建一个Comment对象，但是先不要保存在数据库中
            new_comment = comment_form.save(commit=False)
            # 让当前的post和此comment关联
            new_comment.post = post
            # 保存comment到数据库中
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 获取相似的posts
    # 1. 获取当前post的所有tags
    # 2. 获取这些tags的所有posts
    # 3. 排除当前post
    # 4. 计算post和当前post的共有标签数，并降序排序
    # 5. 同样的共有标签数时，按照publish时间降序排序
    # 6. 切片前几个post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]

    data = dict(
        post=post,
        comments=comments,
        comment_form=comment_form,
        new_comment=new_comment,
        similar_posts=similar_posts
    )

    return render(request,
                  'blog/post/detail.html',
                  data)

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # 发送邮件
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@blog.com', [cd['to']])

            sent = True
    else:
        form = EmailPostForm()
    
    data = dict(
        post=post,
        form=form,
        sent=sent
    )

    return render(request,
                  'blog/post/share.html',
                  data)