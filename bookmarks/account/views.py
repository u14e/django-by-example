from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile

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
    data = dict(
        section='dashboard'
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