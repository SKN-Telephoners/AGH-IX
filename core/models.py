from __future__ import unicode_literals

from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from polymorphic.models import PolymorphicModel

from core.zerotier import Zerotier_API


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)


class BaseConnection(PolymorphicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    assignedIP = models.GenericIPAddressField(null=True, blank=True)

    CONNECTION_TYPE = [
        ("zerotier", "ZeroTier"),
        ("gretap", "GRETAP"),
        ("vxlan", "VXLAN"),
    ]

    STATE = [
        ("connected", "connected"),
        ("disconnected", "disconnected"),
    ]
    asn = models.IntegerField()
    type = models.CharField(choices=CONNECTION_TYPE, max_length=10)
    description = models.CharField(max_length=100, blank=True)
    active = models.CharField(
        choices=STATE, max_length=14, default="disconnected", blank=True
    )


class ZeroTierConnection(BaseConnection):
    zerotier_address = models.CharField(max_length=10)
    zt_api = Zerotier_API()

    def connect(self):
        self.zt_api.post_node_connect(self.zerotier_address)

    def disconnect(self) -> None:
        self.zt_api.post_node(self.zerotier_address, False, False, "0.0.0.0", True)

    def get_ip(self) -> None:
        response: dict = self.zt_api.get_controller_network_member(
            self.zerotier_address
        )
        try:
            self.assignedIP = response["ipAssignments"][0]
        except (IndexError, KeyError):
            pass

    def get_status(self) -> bool:
        response: dict = self.zt_api.get_controller_network_member(
            self.zerotier_address
        )
        try:
            return response["authorized"]
        except KeyError:
            return False

    def is_connected(self) -> bool:
        response_peer: dict = self.zt_api.get_peer(self.zerotier_address)
        response_network: dict = self.zt_api.get_controller_network_member(
            self.zerotier_address
        )
        try:
            return (
                response_network["vMajor"] != -1
                and response_peer["latency"] != -1
                and response_network["authorized"]
            )
        except KeyError:
            return False


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
