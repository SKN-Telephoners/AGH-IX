from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User
from django.contrib.auth import get_user_model

get_user_model()

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=25, required=True)
    surname = forms.CharField(max_length=25, required=True)
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'surname', 'password1', 'password2', )
