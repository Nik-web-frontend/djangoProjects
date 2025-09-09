from django.db import models

# Create your models here.
from django.db import models
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
