from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Post, DeletedPost, Like
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

def register_view(request):
    if request.user.is_authenticated:   # already logged in
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username': '', 'password1': '', 'password2': ''}
        form = UserCreationForm(initial = initial_data)
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:   # already logged in
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request ,data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial = initial_data)
    return render(request, 'auth/login.html', {'form': form})

@login_required(login_url='login')  
def dashboard_view(request):
    posts = Post.objects.all().order_by("-created_at")  # latest first
    for post in posts:
        # check if current user liked this post
        post.is_liked = post.likes.filter(user=request.user).exists()
    return render(request, "dashboard.html", {"posts": posts})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Fetch all posts of logged-in user
    # posts = Post.objects.filter(user=request.user)
    posts = Post.objects.filter(user=request.user).order_by('-created_at')

    if request.method == "POST":
        name = request.POST.get("name")
        profession = request.POST.get("profession")
        profile_pic = request.FILES.get("profile_pic")

        profile.name = name
        profile.profession = profession
        if profile_pic:
            profile.profile_pic = profile_pic
        profile.save()
        return redirect("profile")
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()  # check current user like

    return render(request, "profile.html", {"profile": profile, "posts": posts,  "is_owner": True})


@login_required(login_url='login')
def delete_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile.delete()
        return redirect('dashboard')  # after deleting, go to dashboard (or login page)
    return redirect('profile')  # if not POST, just go back


@login_required(login_url='login')
def upload_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        post_img = request.FILES.get("post_img")
        created_at = models.DateTimeField(auto_now_add=True)

        Post.objects.create(
            user=request.user,
            title=title,
            description=description,
            post_img=post_img
        )

        return redirect("profile")
    return redirect("profile")


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        # DeletedPost me add karo
        DeletedPost.objects.create(post_id=post.id)
        post.delete()
    return redirect("profile")


@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)  # only owner can edit

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        post_img = request.FILES.get("post_img")

        post.title = title
        post.description = description
        if post_img:  # update only if new image uploaded
            post.post_img = post_img
        post.save()

        return redirect("profile")


@login_required(login_url='login')
def search_view(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(user__username__icontains=query) |
            Q(user__userprofile__name__icontains=query)  # if you want full name search
        ).order_by("-created_at")

    return render(request, "search.html", {"results": results, "query": query})    

@login_required(login_url='login')
def user_profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user_obj)
    posts = Post.objects.filter(user=user_obj).order_by("-created_at")

    # check if this is the logged-in user's own profile
    is_owner = (request.user == user_obj)

    return render(request, "profile.html", {
        "profile": profile,
        "posts": posts,
        "is_owner": is_owner,   # pass flag to template
    })


# ----------------------------------------------- 
from django.http import JsonResponse
from django.template.loader import render_to_string
import time

from django.utils import timezone
import datetime

@login_required(login_url='login')
def poll_new_posts(request):
    try:
        # Get the last_check timestamp from request
        last_check = float(request.GET.get("last_check", 0))
        # Convert float timestamp to UTC datetime
        last_check_dt = datetime.datetime.fromtimestamp(last_check, tz=datetime.timezone.utc)
    except (ValueError, TypeError):
        # If invalid, use current time
        last_check_dt = timezone.now()
        last_check = last_check_dt.timestamp()

    # 1️⃣ Check for new or updated posts
    posts = Post.objects.filter(updated_at__gt=last_check_dt).order_by('updated_at')

    post_html = ""
    latest_timestamp = last_check

    if posts.exists():
        for post in posts:
            post_html += render_to_string("post_card.html", {"posts": [post]}, request=request)
            ts = post.updated_at.timestamp()
            if ts > latest_timestamp:
                latest_timestamp = ts

        return JsonResponse({
            "new_post": True,
            "last_check": latest_timestamp,
            "html": post_html
        })

    # 2️⃣ Check for deleted posts
    deleted = DeletedPost.objects.filter(deleted_at__gt=last_check_dt).order_by('deleted_at')
    if deleted.exists():
        deleted_ids = list(deleted.values_list('post_id', flat=True))
        latest_timestamp = deleted.last().deleted_at.timestamp()
        return JsonResponse({
            "deleted_post": True,
            "last_check": latest_timestamp,
            "deleted_ids": deleted_ids
        })

    # 3️⃣ No changes
    return JsonResponse({
        "new_post": False,
        "deleted_post": False,
        "last_check": last_check
    })

# ---------------------  LIKES ----------------------------

@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    like_obj = Like.objects.filter(post=post, user=user).first()
    if like_obj:
        like_obj.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=user)
        liked = True

    # Return updated count
    like_count = post.likes.count()

    return JsonResponse({"liked": liked, "like_count": like_count, "post_id": post_id})