from __future__ import unicode_literals

from uuid import uuid4
from polymorphic.models import PolymorphicModel

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.zerotier import Zerotier_API


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

class BaseConnection(PolymorphicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    CONNECTION_TYPE=[
        ('zerotier', 'ZeroTier'),
        ('gretap', 'GRETAP'),
        ('vxlan', 'VXLAN')
    ]

    STATE=[
        ('connected', 'connected'),
        ('disconnected', 'disconnected'),
    ]
    asn = models.IntegerField()
    type = models.CharField(choices=CONNECTION_TYPE, max_length=10)
    description = models.CharField(max_length=100, blank=True)
    active = models.CharField(choices=STATE, max_length=14, default='disconnected', blank=True)

class ZeroTierConnection(BaseConnection):
    zerotier_address = models.CharField(max_length=10)
    zt_api = Zerotier_API()

    def connect(self):
        self.zt_api.post_node_connect(self.zerotier_address)

    def disconnect(self) -> None:
        self.zt_api.post_node(self.zerotier_address, False, False, "0.0.0.0", True)

    def get_ip(self) -> str:
        response: dict = self.zt_api.get_controller_network_member(self.zerotier_address)
        print(response)
        return response["ipAssignments"][0]

    def get_status(self) -> str:
        response: dict = self.zt_api.get_controller_network_member(self.zerotier_address)
        return response["authorized"]

class GRETAPConnection(BaseConnection):
    ip_address = models.GenericIPAddressField()
    def connect(self):
        pass

    def disconnect(self):
        pass
    
    def get_status(self):
        pass

class VXLANConnection(BaseConnection):
    ip_address = models.GenericIPAddressField()
    def connect(self):
        pass

    def disconnect(self):
        pass
    
    def get_status(self):
        pass
