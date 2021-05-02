from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateCourseForm
from django.utils.text import slugify
from .models import Course

def perfil(request):
    if request.user.is_authenticated:
        cursos_dono = Course.objects.filter(owner=request.user)
        cursos_dict = {'dono': cursos_dono}
        return render(request, 'perfil.html', cursos_dict)
    else:
        return redirect('/homepage')

def criar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateCourseForm(request.POST)
            if form.is_valid():
                # form.save()
                owner = request.user
                subject = form.cleaned_data.get('subject')
                title = form.cleaned_data.get('title')
                overview = form.cleaned_data.get('overview')
                slug = slugify(form.cleaned_data.get('title'))

                curso = Course(owner=owner, subject=subject, title=title, overview=overview, slug=slug)
                curso.save()
                return redirect('/perfil')
        else:
            form = CreateCourseForm()
        return render(request, 'createCurso.html', {'form': form})
    else:
        return redirect('/homepage')

def buscar_cursos(request):
    cursos = Course.objects.all
    cursos_dict = {'cursos': cursos}
    return render(request, 'buscarCursos.html', cursos_dict)