from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm,  InscricaoCurso
from django.shortcuts import render, redirect
from django.contrib import messages

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/genus/inicio')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/genus/inicio')
    else:
        form = RegistrationForm()
    return render(request, 'cadastro.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/genus/inicio')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/genus/inicio')
        else:
            messages.info(request,'Nome de usuário ou senha incorretas')
            return render(request,'login.html')
        
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def check(request):
    print(request.user)
    return render(request, 'index.html')

def recuperar_senha(request):
<<<<<<< HEAD
    return render(request, 'resetPassword.html')
=======
    return render(request, 'resetPassword.html')

# def participar(request, curso_id):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = InscricaoCurso(request.POST)

#             if form.is_valid():
#                 pass
#             else:
#                 #handle invalid form
#                 return redirect('/genus/inicio')
#         else:
#             pass
#     else:
#         pass
>>>>>>> branch_lari
