from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logar, name = 'login'),
    path('cadastro/', views.cadastrar, name = 'cadastro'),
    path('entrou/', views.entrar, name = 'entrou'),
    path('recuperacao/', views.recuperarSenha, name = 'recuperacao'),
    path('validaCadastro/', views.validarCadastro, name = 'validaCadastro'),
    path('validaLogin/', views.validarLogin, name = 'validaLogin'),
    path('alterarSenha/', views.alterarSenha, name = 'alteraSenha'),
]
