from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserProfileForm
from .models import User


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


def register(request):
    """
    用户注册
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！欢迎加入！')
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request, username):
    """
    用户个人主页
    """
    user = User.objects.get(username=username)
    posts = user.posts.all()
    return render(request, 'users/profile.html', {'user': user, 'posts': posts})


def edit_profile(request):
    """
    编辑个人资料
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料更新成功！')
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
