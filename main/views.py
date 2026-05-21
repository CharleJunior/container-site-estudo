import threading
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mural
from django.http import JsonResponse
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Q, Max, Count
from .models import Mensagem, notificacao
from django.shortcuts import get_object_or_404

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

def erro_404(request, exception):
    return render(request, 'errors/404.html', status=404)

@login_required(login_url='login')
def render_home(request):
    aviso = Mural.objects.order_by('-id').first()
    return render(request, 'main/home.html', {'aviso': aviso})


@login_required
def render_msg_section(request):
    user_id = request.GET.get('chat_with')
    contato_selecionado = None
    mensagens = []

    if user_id:
        contato_selecionado = get_object_or_404(User, id=user_id)

        Mensagem.objects.filter(
            remetente=contato_selecionado,
            destinatario=request.user,
            lida=False
        ).update(lida=True)

        notificacao.objects.filter(
            usuario=request.user,
            mensagem_corpo__remetente=contato_selecionado,
            lida=False
        ).update(lida=True)

        mensagens = Mensagem.objects.filter(
            (Q(remetente=request.user) & Q(destinatario=contato_selecionado)) |
            (Q(remetente=contato_selecionado) & Q(destinatario=request.user))
        ).order_by('data_envio')

    usuarios = User.objects.exclude(id=request.user.id).annotate(
        ultima_msg_date=Max(
            'mensagens_enviadas__data_envio',
            filter=Q(mensagens_enviadas__destinatario=request.user) |
                   Q(mensagens_enviadas__remetente=request.user)
        ),
        mensagens_nao_lidas=Count(
            'mensagens_enviadas',
            filter=Q(mensagens_enviadas__destinatario=request.user, mensagens_enviadas__lida=False)
        )
    ).order_by('-ultima_msg_date')

    context = {
        'usuarios': usuarios,
        'contato_selecionado': contato_selecionado,
        'mensagens': mensagens,
    }

    return render(request, 'main/utils/msg_section.html', context)


@login_required
def enviar_mensagem(request, destinatario_id):
    if request.method == 'POST':
        destinatario = get_object_or_404(User, id=destinatario_id)
        conteudo = request.POST.get('conteudo', '').strip()

        if conteudo:
            Mensagem.objects.create(
                remetente=request.user,
                destinatario=destinatario,
                conteudo=conteudo
            )

    return redirect(f"/mensagem/?chat_with={destinatario_id}")


@login_required
def buscar_mensagens(request, contato_id):
    contato = get_object_or_404(User, id=contato_id)

    mensagens = Mensagem.objects.filter(
        (Q(remetente=request.user) & Q(destinatario=contato)) |
        (Q(remetente=contato) & Q(destinatario=request.user))
    ).order_by('data_envio')

    html = render_to_string('main/partials/lista_mensagem.html', {
        'mensagens': mensagens,
        'request': request
    })

    return JsonResponse({'html': html})

@login_required
def checar_notificacoes(request):
    from .models import notificacao
    ultima_notif = notificacao.objects.filter(
        usuario=request.user,
        lida=False
    ).order_by('-data_criacao').first()

    total = notificacao.objects.filter(usuario=request.user, lida=False).count()

    if ultima_notif:
        return JsonResponse({
            'total': total,
            'nova': True,
            'remetente': ultima_notif.mensagem_corpo.remetente.username,
            'texto': ultima_notif.mensagem_corpo.conteudo[:50] + "..."
        })

    return JsonResponse({'total': total, 'nova': False})

@login_required
def apagar_mensagem(request, msg_id):
    mensagem = get_object_or_404(Mensagem, id=msg_id)
    if mensagem.remetente == request.user:
        destinatario_id = mensagem.destinatario.id
        mensagem.delete()
        return redirect(f'/mensagem/?chat_with={destinatario_id}')
    return redirect('/mensagem/')

def pagina_nao_encontrada_customizada(request, exception):
    return render(request, 'errors/erro404.html', status=404)


def fazer_logout(request):
    logout(request)
    return redirect('login')