from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Link this profile to a user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Extra details for profile
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    post_img = models.ImageField(upload_to="post_pics/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} by {self.user.username}"