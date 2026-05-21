from django.urls import path
from main import views

urlpatterns = [
    path('login/', views.render_login, name='login'),
    path('registro/', views.render_registro, name='registro'),
    path('acesso/<str:token>/', views.validar_magic_link, name='validar_magic_link'),
    path('', views.render_home, name='home'),
    path('mensagem/', views.render_msg_section, name='message'),
    path('checar-notificacoes/', views.checar_notificacoes, name='checar_notificacoes'),
    path('enviar/<int:destinatario_id>/', views.enviar_mensagem, name='enviar_mensagem'),
    path('buscar_mensagens/<int:contato_id>/', views.buscar_mensagens, name='buscar_mensagens'),
    path('apagar-mensagem/<int:msg_id>/', views.apagar_mensagem, name='apagar_mensagem'),
    path('logout/', views.fazer_logout, name='logout'),
]
