from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Post

admin.site.register(UserProfile)
admin.site.register(Post)

