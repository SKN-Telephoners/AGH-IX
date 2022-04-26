from __future__ import unicode_literals
from uuid import uuid4

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    bio = models.TextField(max_length=500, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()