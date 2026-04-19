from django.urls import path
from main import views

urlpatterns = [
    path('login/', views.render_login, name='login'),
    path('registro/', views.render_registro, name='registro'),
    path('acesso/<str:token>/', views.validar_magic_link, name='validar_magic_link'),
    path('home/', views.render_home, name='home'),
    path('logout/', views.fazer_logout, name='logout'),
]
