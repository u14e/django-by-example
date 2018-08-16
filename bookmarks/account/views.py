from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

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