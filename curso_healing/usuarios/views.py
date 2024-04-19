from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants, add_message
from django.contrib import auth


# Create your views here.
def cadastrar(request):
    return render(request, "cadastro.html")


def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        print(username, email, senha, confirmar_senha)

        if senha != confirmar_senha:
            add_message(request, constants.ERROR, "Senhas não conferem")
            print("Senhas não conferem")
            return redirect("/usuarios/cadastro")

        if len(senha) < 6:
            add_message(request, constants.ERROR, "Senha muito curta")
            print("Senha muito curta")
            return redirect("/usuarios/cadastro")
        
        user = User.objects.filter(username=username)
        if user.exists():
            add_message(request, constants.ERROR, "Usuário já existe")
            return redirect("/usuarios/cadastro")

        user = User.objects.create_user(username , email, senha)



        return redirect("login")
    

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")

        user = auth.authenticate(request, username=username, password=senha)

        if user is not None:
            auth.login(request, user)
            return redirect('/pacientes/home/')
        else:
            add_message(request, constants.ERROR, "Usuário ou senha inválidos")
            return redirect("/usuarios/login")
        
        
def sair(request):
    auth.logout(request)
    return redirect("/usuarios/login")