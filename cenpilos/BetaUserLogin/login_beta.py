from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect


def login_beta_user(request):
    beta_user = User.objects.get(username='betatest')

    login(request, beta_user)

    return redirect('dashboard')