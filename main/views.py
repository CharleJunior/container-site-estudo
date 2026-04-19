import threading
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mural
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.core.mail import send_mail
from django.urls import reverse

def enviar_magic_link(request, user):
    signer = TimestampSigner()
    last_login_state = str(user.last_login.timestamp() if user.last_login else 0)
    token = signer.sign(f"{user.username}:{last_login_state}")
    link = request.build_absolute_uri(reverse('validar_magic_link', kwargs={'token': token}))

    print(f"E-MAIL PARA: {user.email}")
    print(f"LINK DE ACESSO: {link}")

    def mail_thread():
        send_mail(
            'Link de Acesso',
            f'Acesse aqui: {link}',
            'lwork8017@gmail.com',
            [user.email],
            fail_silently=False,
        )
    threading.Thread(target=mail_thread).start()

def render_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email_digitado = request.POST.get('email')
        user = User.objects.filter(email=email_digitado).first()
        
        if user:
            enviar_magic_link(request, user)
            
        messages.info(request, "Se o e-mail existir, o link foi enviado.")
        return redirect('login')
    
    return render(request, 'main/login/login.html')

def render_registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        
        user_existente = User.objects.filter(email=email).first()

        if user_existente:
            enviar_magic_link(request, user_existente)
            messages.success(request, "Se o e-mail existir, o link foi enviado.")
            return redirect('login')

        if User.objects.filter(username=nome).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return render(request, 'main/login/registro.html')

        novo_user = User.objects.create_user(username=nome, email=email)
        novo_user.set_unusable_password()
        novo_user.save()
        
        enviar_magic_link(request, novo_user)
        messages.success(request, "Cadastro realizado! Verifique seu e-mail.")
        return redirect('login')

    return render(request, 'main/login/registro.html')

def validar_magic_link(request, token):
    signer = TimestampSigner()
    try:
        dados = signer.unsign(token, max_age=1200)
        username, token_last_login = dados.split(':')
        
        user = User.objects.get(username=username)
        current_last_login = str(user.last_login.timestamp() if user.last_login else 0)
        
        if token_last_login != current_last_login:
            messages.error(request, "Este link de acesso já foi utilizado.")
            return redirect('login')

        login(request, user)
        return redirect('home')

    except (SignatureExpired, BadSignature, User.DoesNotExist):
        messages.error(request, "Link expirado ou inválido.")
        return redirect('login')

@login_required
def render_home(request):
    aviso = Mural.objects.order_by('-id').first()
    return render(request, 'main/home.html', {'aviso': aviso})
    

def fazer_logout(request):
    logout(request)
    return redirect('login')