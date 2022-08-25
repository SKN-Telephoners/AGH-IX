from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from core.models import GRETAPConnection, User, VXLANConnection, ZeroTierConnection

get_user_model()


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class ConnectionForm_ZeroTier(ModelForm):
    class Meta:
        model = ZeroTierConnection
        exclude = ["type", "active", "user", "assignedIP"]


class ConnectionForm_VXLAN(ModelForm):
    class Meta:
        model = VXLANConnection
        exclude = ["type", "active", "user", "assignedIP"]

    widgets = {
        "asn": forms.IntegerField(label="Registration Number", widget=forms.TextInput())
    }


class ConnectionForm_GRETAP(ModelForm):
    class Meta:
        model = GRETAPConnection
        exclude = ["type", "active", "user", "assignedIP"]
