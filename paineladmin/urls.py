from django.urls import path
from . import views
urlpatterns = [
        path('admin-painel/', views.render_admin, name='admin'),
        # path('painel/ult-msg/', views.render_ult_msg, name='ult'),
        path('usuarios/', views.lista_usuarios, name='users'),
        path('inicio/', views.render_dashboard, name='dashboard'),
        path('dashboard/log/<int:post_id>/', views.detalhe_log, name='detalhe_log'),
        path('acesso-negado', views.render_erro, name='erro-acesso-negado'),
        # path('painel/mural/', views.render_mural, name='mural_admin'),
        path('alternar-status/<int:user_id>/', views.alternar_status_usuario, name='alternar-acesso')
]