from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import (HttpResponse)
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from blog.forms import SignUpForm
from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_new', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def login(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('post_list'))
            else:
                return HttpResponse("Your account was inactive")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return render(request, 'blog/login.html', {})
    else:
        return render(request, 'blog/login.html', {})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

            return render(request, 'blog/post_list.html', {'posts': posts})
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def account(request):
    user = get_object_or_404(User, username=request.user.username)

    return render(request, 'blog/account.html', {'user': user})


def acc_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("post_list")
