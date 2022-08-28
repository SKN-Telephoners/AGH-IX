from base64 import urlsafe_b64decode, urlsafe_b64encode
from smtplib import SMTPRecipientsRefused

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.messages import constants as messages

from agh_ix.settings import EMAIL_HOST_USER
from core.forms import (
    SignUpForm,
    ConnectionForm_ZeroTier,
    ConnectionForm_GRETAP,
    ConnectionForm_VXLAN,
)
from core.models import User, BaseConnection
from core.tokens import account_activation_token
from core.zerotier import Zerotier_API

get_user_model()


def home(request):
    return render(request, "core/home.html")


@login_required
def network(request):
    network = BaseConnection.objects.filter(user=request.user)
    for connection in network:
        connection.active = "connected" if connection.is_connected() else "disconnected"
        connection.get_ip()

    zt = Zerotier_API()
    host_network = zt.prod_network
    return render(
        request, "core/network.html", {"network": network, "host_network": host_network}
    )


@login_required
def delete_connection(request, ndid):
    zt = Zerotier_API()
    zt.deauth(ndid)
    return redirect("network")


@login_required
def add_connection(request):
    type = request.GET.get("type")
    if request.method == "POST":
        match type:
            case "zerotier":
                form = ConnectionForm_ZeroTier(request.POST)
            case "vxlan":
                form = ConnectionForm_VXLAN(request.POST)
            case "gretap":
                form = ConnectionForm_GRETAP(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.type = type
            obj.save()
            obj.connect()
            return redirect("network")

    match type:
        case "zerotier":
            form = ConnectionForm_ZeroTier
        case "vxlan":
            form = ConnectionForm_GRETAP
        case "gretap":
            form = ConnectionForm_VXLAN
    return render(request, "core/add_connection.html", {"form": form, "type": type})


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False
            user.first_name = form.cleaned_data.get("first_name")
            user.last_surname = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.tmp_email = form.cleaned_data.get("email")
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your AGH-IX account."

            message = render_to_string(
                "registration/acc_activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_b64encode(force_bytes(user.uuid)).decode(),
                    "token": account_activation_token.make_token(user),
                },
            )
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

            return render(
                request,
                "registration/confirm.html",
                {activate: "", "message": "to complete the registration."},
            )
    else:
        form = SignUpForm()
    return render(request, "registration/register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_b64decode(uidb64).decode()
        user = get_object_or_404(User, uuid=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if user.is_active:
            user.email = user.tmp_email
            message = "Your email was changed."
        else:
            user.is_active = True
            message = "Now you can log in into your account."
        user.save()

        return render(request, "registration/activated.html", {"message": message})
    else:
        raise Http404


@login_required
def profile(request):
    return render(request, "users/profile.html")


@login_required
def change_email(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        new_email = request.POST.get("new_email")
        if new_email == request.user.email:
            return render(
                request, "users/email_change.html", {"error": "It's already your email"}
            )
        if user.check_password(request.POST.get("password")):
            request.user.tmp_email = new_email
            request.user.save()
            current_site = get_current_site(request)
            mail_subject = "Change your AGH-IX account's email."
            message = render_to_string(
                "registration/acc_activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_b64encode(force_bytes(user.uuid)).decode(),
                    "token": account_activation_token.make_token(user),
                },
            )
            try:
                send_mail(
                    mail_subject,
                    message,
                    EMAIL_HOST_USER,
                    [new_email],
                    fail_silently=False,
                )
            except SMTPRecipientsRefused:
                pass

            return render(
                request,
                "registration/confirm.html",
                {activate: "", "message": "to complete changing email."},
            )
        else:
            return render(
                request,
                "users/email_change.html",
                {"error": "Wrong password"},
            )
    return render(request, "users/email_change.html")


@login_required
def change_personality(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        if user.check_password(request.POST.get("password")):
            first_name = request.POST.get("new_first_name")
            last_name = request.POST.get("new_last_name")
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            return redirect(profile)
        else:
            return render(request, "users/personality_change.html", {"error": True})
    return render(request, "users/personality_change.html")


@login_required
def del_user(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        if user.check_password(request.POST.get("password")):
            user.delete()
            return redirect("login")
        else:
            return render(request, "users/delete_account.html", {"error": True})
    return render(request, "users/delete_account.html")
