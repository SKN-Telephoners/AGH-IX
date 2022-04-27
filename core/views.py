from base64 import urlsafe_b64decode, urlsafe_b64encode
from smtplib import SMTPRecipientsRefused
from tokenize import Token
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from agh_ix.settings import EMAIL_HOST_USER
from core.forms import SignUpForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from django.contrib.auth import get_user_model
from core.models import User
from core.tokens import account_activation_token
get_user_model()

@login_required
def home(request):
    return render(request, 'core/home.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # load the profile instance created by the signal  
            user.is_active = False
            user.profile.name = form.cleaned_data.get('name')
            user.profile.surname = form.cleaned_data.get('surname')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your AGH-IX account.'

            message = render_to_string('registration/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_b64encode(force_bytes(user.uuid)).decode(),
                'token': account_activation_token.make_token(user),
            })
            try:
                send_mail(
                    mail_subject,
                    message,
                    EMAIL_HOST_USER,
                    [user.profile.email],
                    fail_silently=False,
                )
            except SMTPRecipientsRefused:
                pass

            return render(request, 'registration/confirm.html', {activate: ""})
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_b64decode(uidb64).decode()
        user = get_object_or_404(User, uuid=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, 'registration/activated.html')
    else:
        raise Http404