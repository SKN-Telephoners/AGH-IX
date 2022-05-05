from django.contrib.auth.forms import UserCreationForm
from core.models import User
from django.contrib.auth import get_user_model

get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )
