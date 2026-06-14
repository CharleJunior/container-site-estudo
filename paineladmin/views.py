from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from main.models import Postagem, Comentarios
from django.db.models import Count
# from main.models import Mural
from django.http import JsonResponse
# Create your views here.

def render_admin(request):
    if not request.user.is_staff:
        return redirect('erro-acesso-negado')
    
    return render(request, 'paineladmin/painel.html')

def render_dashboard(request):
    if not request.user.is_staff:
        return redirect('erro-acesso-negado')
    logs_postagens = Postagem.objects.select_related('usuario').order_by('-data_envio')
    
    return render(request, 'utils/dashboard.html', {'logs': logs_postagens})

def detalhe_log(request, post_id):
    if not request.user.is_staff:
        return redirect('erro-acesso-negado')
    
    post = get_object_or_404(
        Postagem.objects.select_related('usuario')
        .prefetch_related('post_comentado__comentarista')
        .annotate(total_comentarios=Count('post_comentado')), 
        id=post_id
    )
    
    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')
    comentarios = post.post_comentado.all().order_by('-data_envio')
        
    return render(request, 'utils/detalhe_log.html', {
        'post': post,
        'comentarios': comentarios
    })
# def render_ult_msg(request):
#     if not request.user.is_staff:
#         return redirect('erro-acesso-negado')
#     # ultimos_avisos = Mural.objects.all().order_by('-data')[:5]
#     return render(request, 'utils/home.html', {'ultimos_avisos': ultimos_avisos})

def render_users(request):
    return render(request, 'utils/users/user.html')

def render_erro(request):
    return render(request, 'utils/users/erros/erro-acesso.html')

# Antiga view para salvar o aviso do admin na tabela de mural
# def salvar_aviso(request):
#     if request.method == 'POST':
#         novo_texto = request.POST.get('texto')
#         Mural.objects.create(
#             texto=novo_texto,
#             autor=request.user
#         )
#         return redirect('admin_painel')

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('username')
    return render(request, 'utils/users/user.html', {'usuarios': usuarios})

# Antiga view para renderizar o mural
# @login_required
# def render_mural(request):
#     if not request.user.is_staff:
#         return redirect('erro-acesso-negado')
#     if request.method == 'POST':
#         novo_texto = request.POST.get('texto')
#         Mural.objects.create(texto=novo_texto, autor=request.user)
#         return redirect('mural_admin')
#     aviso = Mural.objects.last()
#     return render(request, 'utils/mural.html', {'aviso': aviso})

@csrf_exempt
def alternar_status_usuario(request, user_id):
    if request.method == 'POST':
        try:
            usuario = User.objects.get(id=user_id)

            if request.user.id == usuario.id:
                return JsonResponse({
                    'status': 'error',
                }, status=403)

            usuario.is_staff = not usuario.is_staff
            usuario.is_active = True
            usuario.save()

            return JsonResponse({
                'status': 'success',
                'is_staff': usuario.is_staff
            })
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)