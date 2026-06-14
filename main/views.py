import threading
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .models import Mural
from django.http import JsonResponse
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Q, Max, Count
from .models import Mensagem, notificacao
from django.shortcuts import get_object_or_404
from .models import Postagem, Comentarios


 
def enviar_magic_link(request, user):
    """Lógica para enviar a autenticação por email"""
    
    #iniciar o signer, captura estado de ultimo login e monta o token
    signer = TimestampSigner()
    last_login_state = str(user.last_login.timestamp() if user.last_login else 0)
    token = signer.sign(f"{user.username}:{last_login_state}")
    
    #monta o link mágico
    link = request.build_absolute_uri(reverse('validar_magic_link', kwargs={'token': token}))

    #DEBUG PRA CONSOLE
    print(f"E-MAIL PARA: {user.email}")
    print(f"LINK DE ACESSO: {link}")

    #Envia a mensagem para o email digitado
    def mail_thread():
        send_mail(
            'Link de Acesso', #titulo
            f'Acesse aqui: {link}', #mensagem
            'lwork8017@gmail.com', #email postador
            [user.email], #email recebedor
            fail_silently=False, #falha silenciosa (DEBUG)
        )
    threading.Thread(target=mail_thread).start() #roda a thread em segundo plano


def render_login(request):
    """Lógica da renderização da página de login
        - Se o usuario já estiver autenticado, o mesmo será redirecionado
        para a home.
    """
    #Condicional: verifica autenticação
    if request.user.is_authenticated:
        return redirect('home')

    #Condicional: verifica o email digitado, e chama a função para montar uri
    if request.method == 'POST':
        email_digitado = request.POST.get('email')
        user = User.objects.filter(email=email_digitado).first()

        if user:
            enviar_magic_link(request, user)

        messages.info(request, "Se o e-mail existir, o link foi enviado.")
        return redirect('login')

    return render(request, 'main/login/login.html')

def render_registro(request):
    """
        Lógica da renderização da tela de registro
    """
    
    #Condicional: verifica autenticação
    if request.user.is_authenticated:
        return redirect('home')

    #Condicional: verifica nome e email digitado, cria o usuario e salva no banco 
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')

        user_existente = User.objects.filter(email=email).first()
        
        #Condicional: envia email para acesso
        if user_existente:
            enviar_magic_link(request, user_existente)
            messages.success(request, "Se o e-mail existir, o link foi enviado.")
            return redirect('login')

        #Condicional: tratamento de erro caso o nome de usuario já esteja em uso
        if User.objects.filter(username=nome).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return render(request, 'main/login/registro.html')

        #cria e salva o usuario no banco
        novo_user = User.objects.create_user(username=nome, email=email)
        novo_user.set_unusable_password()
        novo_user.save()

        #envia o link
        enviar_magic_link(request, novo_user)
        messages.success(request, "Cadastro realizado! Verifique seu e-mail.")
        return redirect('login')

    return render(request, 'main/login/registro.html')

def validar_magic_link(request, token):
    """Valida o tempo limite do magic link"""
    
    #inicia o signer
    signer = TimestampSigner()
    try:
        #tempo limite do token: 1200 segundos
        dados = signer.unsign(token, max_age=1200)
        username, token_last_login = dados.split(':')

        user = User.objects.get(username=username)
        #ternário que verifica se o usuario já logou antes, se não, 0
        current_last_login = str(user.last_login.timestamp() if user.last_login else 0)

        #Condicional: compara o token_last_login com current_last_login, se forem diferentes o link já foi usado
        if token_last_login != current_last_login:
            messages.error(request, "Este link de acesso já foi utilizado.")
            return redirect('login')

        login(request, user)
        return redirect('home')

    except (SignatureExpired, BadSignature, User.DoesNotExist):
        messages.error(request, "Link expirado ou inválido.")
        return redirect('login')

@login_required(login_url='login')
def render_home(request):
    #variavel de antigo mural
    #aviso = Mural.objects.order_by('-id').first()
    
    #lógica para pegar todos os posts
    if request.method == 'POST':
        texto_digitado = request.POST.get('conteudo')
        imagem_enviada = request.FILES.get('imagem') 
       
        if texto_digitado:
            Postagem.objects.create(
                texto = texto_digitado,
                imagem = imagem_enviada,
                usuario = request.user,
            )
            messages.success(request, 'Postagem publicada!')
            return redirect ('home')
        
    postagens = Postagem.objects.all()
    return render(request, 'main/home.html', {'postagens':postagens})

def detalhes(request, post_id):
    """Função para ver detalhadamente a postagem e os comentarios"""
    postagem = get_object_or_404(Postagem, id=post_id)
    if request.method == 'POST':
        texto_comentario_digitado = request.POST.get('conteudo_comentario')
        
        if texto_comentario_digitado:
            Comentarios.objects.create(
                comentario = texto_comentario_digitado,
                comentarista = request.user,
                postagem = postagem
            )
            
            return redirect('ver_comentarios', post_id=post_id)
    
    comentarios = Comentarios.objects.all()
    context = {
        'comentarios':comentarios,
        'post':postagem
    }  
    return render(request, 'main/utils/detalhes.html', context)            

def deletar_comentarios(request, comentarios_id):
    """Função para poder apagar os comentarios, apenas os proprios usuarios e admins podem fazer isso"""
    comentarios = get_object_or_404(Comentarios, id=comentarios_id)
    post_id = comentarios.postagem.id
    if comentarios.comentarista == request.user or request.user.is_staff:
        comentarios.delete()
        messages.success(request, 'Comentario apagado')
    return redirect('ver_comentarios', post_id=post_id)    

@login_required(login_url='login')
def deletar_post(request, post_id):
    """Função para deletar posts, apenas os próprios usuários donos dos posts
    e admins podem apagar"""
    
    post = get_object_or_404(Postagem, id=post_id)
    if post.usuario == request.user or request.user.is_staff:
        post.delete()
        messages.success(request, 'Post deletado')
    return redirect ('home')    
    
@login_required
def render_msg_section(request):
    """Renderiza sessão de mensagens entre os usuarios"""
    user_id = request.GET.get('chat_with')
    contato_selecionado = None
    mensagens = []

    #Condicional: procura o usuario clicado
    if user_id:
        contato_selecionado = get_object_or_404(User, id=user_id)

        #Objeto da mensagem
        Mensagem.objects.filter(
            remetente=contato_selecionado,
            destinatario=request.user,
            lida=False
        ).update(lida=True)

        #Objeto da notificação
        notificacao.objects.filter(
            usuario=request.user,
            mensagem_corpo__remetente=contato_selecionado,
            lida=False
        ).update(lida=True)

        #filtra o objeto da mensagem procurando todo o histórico entre o destinatario e o remetente
        #ordena pela data de envio
        mensagens = Mensagem.objects.filter(
            (Q(remetente=request.user) & Q(destinatario=contato_selecionado)) |
            (Q(remetente=contato_selecionado) & Q(destinatario=request.user))
        ).order_by('data_envio')
    
    
    #exlui o proprio remetente da lista de contatos
    #pega a data da ultima mensagem enviada entre o rementente e destinatário
    #conta a quantidade de mensagems do destinatario não lidas
    #ordena pela mensagem mais recente
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
    """Monta e envia a mensagem"""
    
    #Condicional: busca o destinatario e o conteudo escrito na mensagem
    if request.method == 'POST':
        destinatario = get_object_or_404(User, id=destinatario_id)
        conteudo = request.POST.get('conteudo', '').strip()

        #Condicional: monta a mensagem
        if conteudo:
            Mensagem.objects.create(
                remetente=request.user,
                destinatario=destinatario,
                conteudo=conteudo
            )

    return redirect(f"/mensagem/?chat_with={destinatario_id}")


@login_required
def buscar_mensagens(request, contato_id):
    """Lógica para buscar as mensagens dos usuários"""
    contato = get_object_or_404(User, id=contato_id)

    #Procura o histórico de mensagens entre o remetente e o destinatario
    #ordena pela mais recente
    #guarda o html da mensagem enviada em um Json 
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
    """Lógica para checar notificações"""
    from .models import notificacao
    
    #busca o historico de notificações, e pega a mais recente
    ultima_notif = notificacao.objects.filter(
        usuario=request.user,
        lida=False
    ).order_by('-data_criacao').first()

    #busca o historico de notificações não lidas e soma a quantidade
    total = notificacao.objects.filter(usuario=request.user, lida=False).count()

    #monta a notificação
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
    """Lógica para a apagar as mensagens"""
    mensagem = get_object_or_404(Mensagem, id=msg_id)
    
    #Condicional: busca e deleta a mensagem
    if mensagem.remetente == request.user:
        destinatario_id = mensagem.destinatario.id
        mensagem.delete()
        return redirect(f'/mensagem/?chat_with={destinatario_id}')
    return redirect('/mensagem/')

#erro 404
def pagina_nao_encontrada_customizada(request, exception):
    return render(request, 'errors/erro404.html', status=404)

#logout
def fazer_logout(request):
    logout(request)
    return redirect('login')