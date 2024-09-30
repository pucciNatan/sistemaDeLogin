from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuarios
from hashlib import sha256

def entrar(req):
    if req.session.get('logado'):
        nome = req.GET.get('nome')
        tempoExpiraSessao = req.session.get_expiry_age()
        return render(req, 'entrou.html', {'nome': nome, 'tempoExpiraSessao': tempoExpiraSessao})
    else:
        return redirect('/auth/login/')

def logar(req):
    status = req.GET.get('status')
    return render(req, 'login.html', {'status': status})

def cadastrar(req):
    status = req.GET.get('status')
    return render(req, 'cadastro.html', {'status': status})

def recuperarSenha(req):
    status = req.GET.get('status')
    email = req.GET.get('email')

    #Senha curta é sempre '0', serve para mandar uma mensagem na tela do usuário (HTML) pedindo pra inserir uma maior.
    senhaCurta = req.GET.get('senhaCurta')

    return render(req, 'recuperacao.html', {'status': status, 'email': email, 'senhaCurta': senhaCurta})

def validarLogin(req):
    email = req.POST.get('email')
    senha = req.POST.get('senha')

    senhaCriptografada = sha256(senha.encode()).hexdigest()

    usuariosFiltrados = Usuarios.objects.filter(email = email).filter(senha = senhaCriptografada)

    if usuariosFiltrados.exists():
        nome = usuariosFiltrados[0].nome  
        req.session['logado'] = True
        return redirect(f'/auth/entrou/?nome={nome}')

    else:
        return redirect('/auth/login/?status=1')

def validarCadastro(req):
    nome = req.POST.get('nome')
    email = req.POST.get('email')
    senha = req.POST.get('senha')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    usuariosFiltrados = Usuarios.objects.filter(email = email)
    if usuariosFiltrados.exists():
        return redirect('/auth/cadastro/?status=2')
    
    if len(senha) < 6:
        return redirect('/auth/cadastro/?status=3')
    
    senhaCriptografada = sha256(senha.encode()).hexdigest()

    try:
        usuario = Usuarios(nome = nome, email = email, senha = senhaCriptografada)

        usuario.save()
        return redirect('/auth/cadastro/?status=0')
    
    except:
        return redirect('/auth/cadastro/?status=4')
    
def alterarSenha(req):

    if 'email' in req.POST:
        email = req.POST.get('email')

        usuariosFiltrados = Usuarios.objects.filter(email = email)

        if len(email) == 0:
            return redirect('/auth/recuperacao/?status=2')
        elif usuariosFiltrados.exists():
            return redirect(f'/auth/recuperacao/?status=0&email={email}')
        else:
            return redirect('/auth/recuperacao/?status=1')

    elif 'novaSenha' in req.POST:
        novaSenha = req.POST.get('novaSenha')
        emailEncontrado = req.POST.get('emailEncontrado')

        if len(novaSenha) < 6:
            return redirect('/auth/recuperacao/?status=0&email=natan.puccib@gmail.com&senhaCurta=0')

        novaSenhaCriptografada = sha256(novaSenha.encode()).hexdigest()

        usuarioFiltrado = Usuarios.objects.filter(email = emailEncontrado).first()
        usuarioFiltrado.senha = novaSenhaCriptografada

        usuarioFiltrado.save()

        return redirect('/auth/login')   
    