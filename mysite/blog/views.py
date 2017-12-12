from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.core.mail import send_mail
from django.db.models import Count

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from haystack.query import SearchQuerySet


class PostListView(generic.ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(req, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 每页三篇
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果page超出总页数，返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(req,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(req, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)

    # 相似文章
    # values_list()返回queryset中包含指定字段的元组，flat获取简单列表
    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#values-list
    post_tags_ids = post.tags.values_list('id', flat=True)
    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#in
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#annotate
    # https://docs.djangoproject.com/en/1.11/topics/db/aggregation/
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    if req.method == 'POST':
        comment_form = CommentForm(data=req.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(req, 'blog/post/detail.html', {'post': post,
                                                 'comments': comments,
                                                 'comment_form': comment_form,
                                                 'similar_posts': similar_posts})


def post_share(req, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if req.method == 'POST':
        form = EmailPostForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = req.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends your reading "{}"'.format(
                cd['name'], cd['email'], post.title
            )
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comments']
            )
            send_mail(subject, message, '15521195447@163.com', [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(req, 'blog/post/share.html', {'post': post,
                                                'form': form,
                                                'sent': sent})


def post_search(req):
    form = SearchForm()
    if 'query' in req.GET:
        form = SearchForm(req.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post) \
                .filter(content=cd['query']).load_all()
            total_results = results.count()
        return render(req, 'blog/post/search.html', {'form': form,
                                                     'cd': cd,
                                                     'results': results,
                                                     'total_results': total_results})
    return render(req, 'blog/post/search.html', {'form': form})


def test(req):
    form = EmailPostForm()
    if req.method == 'POST':
        print(req.POST)
    return render(req, 'test.html', {'form': form})
