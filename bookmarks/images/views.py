import redis
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from common.decorators import ajax_required
from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image

pool = redis.ConnectionPool(host=settings.REDIS_HOST,
                            port=settings.REDIS_PORT,
                            db=settings.REDIS_DB,
                            decode_responses=True)
r = redis.StrictRedis(connection_pool=pool)

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            
            create_action(request.user, 'bookmarked image', new_item)

            messages.success(request, '图片添加成功')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    
    data = dict(
        section='images',
        form=form
    )

    return render(request,
                  'images/image/create.html',
                  data)

@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # 总阅读数(每次自增1)
    total_views = r.incr('image:{}:views'.format(image.id))
    # 构建有序集合，每次将image_ranking下面的image.id自增1
    r.zincrby('image_ranking', image.id, 1)
    data = dict(
        image=image,
        total_views=total_views
    )
    
    return render(request,
                  'images/image/detail.html',
                  data)

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            data = dict(
                status='ok'
            )
            return JsonResponse(data)
        except:
            pass

    data = dict(
        status='ko'
    )
    return JsonResponse(data)

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        # 如果是ajax请求，并且超出总页数，返回空。否则返回最后一页
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    
    data = dict(
        section='images',
        images=images
    )

    # ajax请求返回片段
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      data)

    return render(request,
                  'images/image/list.html',
                  data)

@login_required
def image_ranking(request):
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10] # 获取图片浏览量前十的图片集合
    image_ranking_ids = [int(id) for id in image_ranking]   # 获取集合中的id
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))  # 通过id获取对应的Image列表
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))   # 对列表排序

    data = dict(
        section='images',
        most_viewed=most_viewed
    )
    return render(request,
                  'images/image/ranking.html',
                  data)