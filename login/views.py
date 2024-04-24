from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import MyUser
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

import ssl



ssl._create_default_https_context = ssl._create_unverified_context




#----------------LOGIN------------------#
@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('app_almoxarifado:menu')
    else:
        context = {}

        return render(request, 'login/login.html', context)
@csrf_exempt
def logar(request):
    user = authenticate(request, username=request.POST['login'], password=request.POST['senha'])
    if user is not None:
        auth_login(request, user)
        return redirect('app_almoxarifado:menu')
    else:
        messages.error(request, 'Usuário ou senha incorretos.') # Adiciona uma mensagem de erro
        return redirect('login:login')

@csrf_exempt
def log_out(request):
    logout(request)
    return redirect('/')
    # Redirect to a success page.

