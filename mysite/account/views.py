from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


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
            return render(req, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(req, 'account/register.html', {'user_form': user_form})


@login_required
def dashboard(req):
    return render(req, 'account/dashboard.html', {'section': 'dashboard'})


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

