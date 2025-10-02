from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.login_view, name='default_screen'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path("upload_post/", views.upload_post, name="upload_post"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("search/", views.search_view, name="search"),
    path("profile/<str:username>/", views.user_profile_view, name="user-profile"),
    path("poll_new_posts/", views.poll_new_posts, name="poll_new_posts"),
    path("toggle_like/<int:post_id>/", views.toggle_like, name="toggle_like"),

]