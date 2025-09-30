from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Post
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

def poll_new_posts(request):
    last_check = float(request.GET.get("last_check", 0))
    timeout = 15
    start = time.time()

    from .models import Post

    while True:
        latest_post = Post.objects.order_by('-created_at').first()

        if latest_post and latest_post.created_at.timestamp() > last_check:
         
            html = render_to_string("post_card.html", {"posts": [latest_post]}, request=request)

            return JsonResponse({
                "new_post": True,
                "post_id": latest_post.id,   # 👈 important for duplicate check in JS
                "last_check": latest_post.created_at.timestamp(),
                "html": html
            })

        if time.time() - start > timeout:
            return JsonResponse({"new_post": False, "last_check": time.time()})

        time.sleep(1)
