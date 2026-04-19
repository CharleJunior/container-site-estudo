from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from main.models import Mural
from django.http import JsonResponse
# Create your views here.

def render_admin(request):
    if not request.user.is_staff:
        return redirect('erro-acesso-negado')
    return render(request, 'paineladmin/painel.html')

def render_ult_msg(request):
    if not request.user.is_staff:
        return redirect('erro-acesso-negado')
    ultimos_avisos = Mural.objects.all().order_by('-data')[:5]
    return render(request, 'utils/home.html', {'ultimos_avisos': ultimos_avisos})

def render_users(request):
    return render(request, 'utils/users/user.html')

def render_erro(request):
    return render(request, 'utils/users/erros/erro-acesso.html')

def salvar_aviso(request):
    if request.method == 'POST':
        novo_texto = request.POST.get('texto')
        Mural.objects.create(
            texto=novo_texto,
            autor=request.user 
        )
        return redirect('admin_painel')

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('username') 
    return render(request, 'utils/users/user.html', {'usuarios': usuarios})

@login_required
def render_mural(request):
    if not request.user.is_staff:
        return redirect('erro-acesso-negado')
    if request.method == 'POST':
        novo_texto = request.POST.get('texto')
        Mural.objects.create(texto=novo_texto, autor=request.user)
        return redirect('mural_admin') 
    aviso = Mural.objects.last()
    return render(request, 'utils/mural.html', {'aviso': aviso})

@csrf_exempt
def alternar_status_usuario(request, user_id):
    if request.method == 'POST':
        try:
            usuario = User.objects.get(id=user_id)
            usuario.is_staff = not usuario.is_staff
            usuario.is_active = True       
            usuario.save()
            
            return JsonResponse({
                'status': 'success', 
                'is_staff': usuario.is_staff 
            })
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)