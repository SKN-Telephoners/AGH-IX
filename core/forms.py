from unicodedata import name
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=25, required=True)
    surname = forms.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'surname', 'password1', 'password2', )