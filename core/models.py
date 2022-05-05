from __future__ import unicode_literals
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
