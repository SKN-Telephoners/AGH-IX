"""agh_ix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views

from core import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('register/', core_views.register, name='register'),
    path('network/', core_views.network, name='network'),
    path('add_connection/', core_views.add_connection, name='add_connection'),
    path('activate/<uidb64>/<token>', core_views.activate, name='activate'),
    path('admin/', admin.site.urls),
    path('password_change/', auth_views.PasswordChangeView.as_view() , name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view() , name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view() , name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view() , name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view() , name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view() , name='password_reset_complete'),
]
