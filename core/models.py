from __future__ import unicode_literals

from abc import ABC, abstractmethod
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.zerotier import Zerotier_API


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


class BaseConnection(ABC):
    @abstractmethod
    def __init__(self, asn, type, description):
        self.asn: str = asn
        self.type: str = type
        self.description: str = description

    @abstractmethod
    def connect(self) -> str:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def get_ip(self) -> str:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass


class ZeroTierConnection(BaseConnection):
    def __init__(self, asn, address):
        self.address = address
        self.zt_api: Zerotier_API = Zerotier_API.get_instance()
        type = "ZeroTier"
        super().__init__(asn, type)
    
    def connect(self) -> str:
        self.zt_api.post_node(self.address)
        return self.get_ips()[0]

    def disconnect(self) -> None:
        self.zt_api.post_node(self.address, False, False, "0.0.0.0", False)

    def get_ip(self) -> str:
        response: dict = self.zt_api.get_controller_network_member(self.address)
        return response["config"]["ipAssignments"][0]

    def get_status(self) -> str:
        response: dict = self.zt_api.get_controller_network_member(self.address)
        return response["config"]["authorized"]

class GRETAPConnection(BaseConnection):
    def connect(self):
        pass

    def disconnect(self):
        pass
    
    def get_status(self):
        pass

class VXLANConnection(BaseConnection):
    def connect(self):
        pass

    def disconnect(self):
        pass
    
    def get_status(self):
        pass
