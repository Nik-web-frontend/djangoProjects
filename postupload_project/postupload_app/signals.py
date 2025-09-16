from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from .models import Post, UserProfile

@receiver(post_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    if instance.post_img and os.path.isfile(instance.post_img.path):
        os.remove(instance.post_img.path)

@receiver(post_delete, sender=UserProfile)
def delete_profile_image(sender, instance, **kwargs):
    if instance.profile_pic and os.path.isfile(instance.profile_pic.path):
        os.remove(instance.profile_pic.path)
