from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from common.decorators import ajax_required
from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image

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

    data = dict(
        image=image
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