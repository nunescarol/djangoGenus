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
    if request.user.is_authenticated:
        cursos = Course.objects.all
        cursos_dict = {'cursos': cursos}
        return render(request, 'buscarCursos.html', cursos_dict)
    else:
        return redirect('/homepage')

def resumo(request, curso_id):
    try:
        c= Course.objects.get(pk=curso_id)
    except Course.DoesNotExist:
        raise Http404("Encontramos um erro")
    return render(request, 'resumoCurso.html', {'curso':c})


    # if request.user.is_authenticated:
    #     curso = Course.objects.filter(title=curso_title)
    #     cursos_dict = {'curso_selecionado': curso}
    #     for cursos in curso_selecionado:
    #         print(cursos)
    #     return render(request, 'resumoCurso.html', {'curso_selecionado':curso})
    # else:
    #     return redirect('/homepage')
