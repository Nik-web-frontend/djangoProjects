from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile

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
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        profession = request.POST.get("profession")
        profile_pic = request.FILES.get("profile_pic")

        # Check if user already has a profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.name = name
        profile.profession = profession
        if profile_pic:
            profile.profile_pic = profile_pic
        profile.save()

        return redirect("profile")  # reload profile page

    else:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return render(request, "profile.html", {"profile": profile})
    


@login_required(login_url='login')
def delete_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile.delete()
        return redirect('dashboard')  # after deleting, go to dashboard (or login page)
    return redirect('profile')  # if not POST, just go back

