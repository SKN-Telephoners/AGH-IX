from base64 import urlsafe_b64decode, urlsafe_b64encode
from smtplib import SMTPRecipientsRefused
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from agh_ix.settings import EMAIL_HOST_USER
from core.forms import SignUpForm, ConnectionForm_ZeroTier, ConnectionForm_GRETAP, ConnectionForm_VXLAN
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from core.models import User, BaseConnection
from core.tokens import account_activation_token

get_user_model()

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def network(request):
    network = BaseConnection.objects.filter(user=request.user)
    return render(request, 'core/network.html', {'network': network})

@login_required
def add_connection(request):
    type = request.GET.get('type')
    if request.method == 'POST':
        match type:
            case 'zerotier':
                form = ConnectionForm_ZeroTier(request.POST)
            case 'vxlan':
                form = ConnectionForm_VXLAN(request.POST)
            case 'gretap':
                form = ConnectionForm_GRETAP(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.type = type
            obj.save()
            obj.connect()
            return redirect('network')
            
    match type:
        case 'zerotier':
            form = ConnectionForm_ZeroTier
        case 'vxlan':
            form = ConnectionForm_GRETAP
        case 'gretap':
            form = ConnectionForm_VXLAN
    return render(request, 'core/add_connection.html', {'form': form, 'type': type})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False
            user.first_name = form.cleaned_data.get('first_name')
            user.last_surname = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
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
                    [user.email],
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