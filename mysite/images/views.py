from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

import redis
from django.conf import settings

from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action

# 连接redis
# 参看http://www.jianshu.com/p/2639549bedc8
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB,
                      decode_responses=True)


@login_required
def image_create(req):
    if req.method == 'POST':
        form = ImageCreateForm(data=req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = req.user
            new_item.save()
            create_action(req.user, 'bookmarked image', new_item)  # 添加进活动流
            messages.success(req, '图片添加成功')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=req.GET)
    return render(req, 'images/image/create.html', {'section': 'images',
                                                    'form': form})


def image_detail(req, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr('image:{}:views'.format(image.id))  # 图片总浏览数
    r.zincrby('image_ranking', image.id, 1)  # 自增id对应的有序集合id
    return render(req, 'images/image/detail.html', {'section': 'images',
                                                    'image': image,
                                                    'total_views': total_views})


@ajax_required
@login_required
@require_POST
def image_like(req):
    """
    图片点赞的ajax请求
    :param req:
    :return:
    """
    image_id = req.POST.get('id')
    action = req.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(req.user)
                create_action(req.user, 'likes', image)  # 添加进活动流
            else:
                image.users_like.remove(req.user)
                create_action(req.user, 'unlikes', image)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(req):
    images = Image.objects.all().order_by('created')
    paginator = Paginator(images, 8)
    page = req.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，返回第一页
        images = paginator.page(1)
    except EmptyPage:
        # 如果是ajax请求以及page超出总页数，返回一个空页
        if req.is_ajax():
            return HttpResponse('')
        # 如果page超出总页数，返回最后一页
        images = paginator.page(paginator.num_pages)

    if req.is_ajax():
        return render(req, 'images/image/list_ajax.html', {'section': 'images',
                                                           'images': images})

    return render(req, 'images/image/list.html', {'section': 'images',
                                                  'images': images})


@login_required
def image_ranking(req):
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:3]  # 获取图片浏览量前十的图片集合
    image_ranking_ids = [int(id) for id in image_ranking]  # 获取集合中的id
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))  # 通过id获取对应的Image
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))  # 排序
    for i, id in enumerate(image_ranking_ids):
        most_viewed[i].views = r.get('image:{}:views'.format(id)) or 0
    return render(req, 'images/image/ranking.html', {'section': 'images',
                                                     'most_viewed': most_viewed})
