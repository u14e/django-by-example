from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from actions.utils import create_action

from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile, Contact
from actions.models import Action

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('认证成功')
                else:
                    return HttpResponse('用户无效')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    
    data = dict(
        form=form
    )

    return render(request, 'account/login.html', data)

@login_required
def dashboard(request):
    # 默认获取除自己以外的所有actions
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        # 如果follow别人，则只获取这些人的actions
        actions = actions.filter(user_id__in=following_ids)
    
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]

    data = dict(
        section='dashboard',
        actions=actions
    )
    return render(request,
                  'account/dashboard.html',
                  data)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # 创建Profile
            Profile.objects.create(user=new_user)

            create_action(new_user, 'has created an account')

            data = dict(
                new_user=new_user
            )
            return render(request,
                          'account/register_done.html',
                          data)
    else:
        user_form = UserRegistrationForm()
    
    data = dict(
        user_form=user_form
    )
    return render(request,
                  'account/register.html',
                  data)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile更新成功')
        else:
            messages.error(request, 'Profile更新失败')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    data = dict(
        user_form=user_form,
        profile_form=profile_form
    )

    return render(request,
                  'account/edit.html',
                  data)

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    data = dict(
        section='people',
        users=users
    )
    return render(request,
                  'account/user/list.html',
                  data)

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    data = dict(
        section='people',
        user=user
    )
    return render(request,
                  'account/user/detail.html',
                  data)

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})