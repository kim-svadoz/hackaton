from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Profile
from .forms import ProfileForm
from django.contrib.auth import get_user_model
from django.contrib import messages

import requests
import json

# Create your views here.
def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                Profile.objects.create(user = user)
                auth_login(request, user)
                messages.success(request, '회원가입 완료')
                return redirect('accounts:index')
            else:
                messages.error(request, '회원가입 못했어요 엉엉~')
        else:
            form = UserCreationForm()
        context = {
            'form' : form
        }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                messages.success(request, '로그인 완료')
                return redirect(request.GET.get('next') or 'accounts:index')
            else:
                messages.error(request, '로그인 못했어요 엉엉~')
        else:
            form = AuthenticationForm
        context={
            'form' : form
        }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

def profile(request, username):
    person = get_object_or_404(get_user_model(), username = username)
    context = {
        'person' : person
    }
    return render(request, 'accounts/profile.html', context)

def profile_update(request):
    if request.user.profile:
        profile = request.user.profile
        if request.method =='POST':
            form = ProfileForm(request.POST, request.FILES, instance = profile)
            if form.is_valid:
                form.save()
                messages.success(request, '프로필 수정 완료')
                return redirect('accounts:profile', request.user.username)
            else:
                messages.error(request, '회원가입 못했어요 엉엉~')
        else:
            form = ProfileForm(instance = profile)
    else:
        Profile.objects.create(user = request.user)
        form = ProfileForm(request.POST, request.FILES, instance = profile)
    context = {
            'form' : form
        }
    return render(request, 'accounts/profile_update.html', context)

@login_required
def delete(request):
    request.user.delete()
    return redirect('accounts:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '개인정보 수정 완료')
            return redirect('accounts:index')
        else:
            messages.success(request, '개인정보 수정 못했어요 엉엉~')
    else:
        form = CustomUserChangeForm(instance = request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호 변경 완료')
            return redirect('accounts:index')
        else:
            messages.success(request, '비밀번호 변경 못했어요 엉엉ㅠ')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/password.html', context)