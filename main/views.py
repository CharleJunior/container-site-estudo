from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mural

def render_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        usuario = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Usuário ou senha incorretos.")
            return render(request, 'main/login/login.html')

    return render(request, 'main/login/login.html')

def render_registro(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_confirm = request.POST.get('confirmar_senha')
        
        if User.objects.filter(username=nome).exists():
            messages.error(request, "Este nome de usuário já existe.")
            return render(request, 'main/login/registro.html')
        
        if senha != senha_confirm:
            messages.error(request, "As senhas não coincidem!")
            return render(request, 'main/login/registro.html')
        
        novo_user = User.objects.create_user(username=nome, email=email, password=senha)
        novo_user.save()
        return redirect('home') 
    return render(request, 'main/login/registro.html')

@login_required
def render_home(request):
    aviso = Mural.objects.last()
    
    return render(request, 'main/home.html', {'aviso': aviso})


def fazer_logout(request):
    logout(request)
    return redirect('login')