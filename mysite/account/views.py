from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from actions.utils import create_action
from actions.models import Action


def user_login(req):
    """
    # 自定义的用户登陆
    """
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(req, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(req, 'account/login.html', {'form': form})


def register(req):
    """
    自定义的用户注册
    """
    if req.method == 'POST':
        user_form = UserRegistrationForm(req.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')  # 添加进活动流
            return render(req, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(req, 'account/register.html', {'user_form': user_form})


@login_required
def dashboard(req):
    actions = Action.objects.exclude(user=req.user)
    following_ids = req.user.following.values_list('id', flat=True)
    if following_ids:
        # select_related支持OneToOne,ForeignKey(one to many)
        # prefetch_related支持ManyToMany，反向ForeignKey(many to one)
        actions = actions.filter(user_id__in=following_ids) \
            .select_related('user', 'user__profile') \
            .prefetch_related('target')

    actions = actions[:10]

    return render(req, 'account/dashboard.html', {'section': 'dashboard',
                                                  'actions': actions})


@login_required
def edit(req):
    if req.method == 'POST':
        user_form = UserEditForm(instance=req.user,
                                 data=req.POST)
        profile_form = ProfileEditForm(instance=req.user.profile,
                                       data=req.POST,
                                       files=req.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(req, 'profile更新成功')
        else:
            messages.error(req, 'profile更新失败')
    else:
        user_form = UserEditForm(instance=req.user)
        profile_form = ProfileEditForm(instance=req.user.profile)
    return render(req, 'account/edit.html', {'user_form': user_form,
                                             'profile_form': profile_form})


@login_required
def user_list(req):
    users = User.objects.filter(is_active=True)
    return render(req, 'account/user/list.html', {'section': 'people',
                                                  'users': users})


@login_required
def user_detail(req, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(req, 'account/user/detail.html', {'section': 'people',
                                                    'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(req):
    user_id = req.POST.get('id')
    action = req.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=req.user, user_to=user)
                create_action(req.user, 'is following', user)  # 添加进活动流
            else:
                Contact.objects.filter(user_from=req.user, user_to=user).delete()
                create_action(req.user, 'unfollow', user)  # 添加进活动流
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
