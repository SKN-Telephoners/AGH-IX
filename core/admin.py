from django.contrib import admin
from core.models import GRETAPConnection, User, BaseConnection, VXLANConnection, ZeroTierConnection
from core.views import register

admin.site.register(User)
admin.site.register(BaseConnection)
admin.site.register(GRETAPConnection)
admin.site.register(VXLANConnection)
admin.site.register(ZeroTierConnection)
