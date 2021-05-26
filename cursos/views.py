from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import path, reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Q
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.views.generic import ListView

from .forms import CreateCourseForm, CreateActivityForm, CreatePostForm, CreateModuleForm, AddFileForm, AddImageForm, EscolhaTipo, AddTextForm, AddVideoForm, CommentForm

from .models import Course, Module, Content, Activity, Post, Comment
from registro.forms import InscricaoCurso



def inicio(request):
    if request.user.is_authenticated:
        cursos_dono = Course.objects.filter(owner=request.user)
        c = Course.objects.all()
        cursos_matriculado = []
        for curso in c:
            if request.user in curso.students.all():
                cursos_matriculado.append(curso)

        cursos_dict = {'dono': cursos_dono,
                        'cursos': c,
                        'matriculado': cursos_matriculado,     
                    }
        return render(request, 'inicio.html', cursos_dict)
    else:
        return redirect('/')

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
                return redirect('/genus/inicio/')

            else:
                #handle invalid form
                form = CreateCourseForm()
                return render(request, 'createCurso.html', {'form': form})
        else:
            form = CreateCourseForm()
            return render(request, 'createCurso.html', {'form': form})
    else:
        return redirect('/')

def buscar_cursos(request):
    if request.user.is_authenticated:
        cursos = Course.objects.all()
        cursos_paginator = Paginator(cursos, 1)
        num_pagina = request.GET.get('paginas')
        paginas = cursos_paginator.get_page(num_pagina)
        

        if request.method == 'POST':
            search = request.POST['search']
            cursos = Course.objects.filter(Q(title__contains=search) | Q(overview__contains=search) | Q(subject__title__contains=search) | Q(title__contains=search) | Q(owner__username__contains=search))
            cursos_paginator = Paginator(cursos, 1)
            num_pagina = request.GET.get('paginas')
            paginas = cursos_paginator.get_page(num_pagina)
            print(cursos)
            return render(request, 'buscarCursos.html', {'cursos': cursos, 'paginas': paginas, 'search': search})
        
        return render(request, 'buscarCursos.html', {'cursos': cursos, 'paginas': paginas,})
    else:
        return redirect('/')

def resumo(request, curso_slug):
    
    ##com função de participar
    if request.user.is_authenticated:
        try:
            c= Course.objects.get(slug=curso_slug)
        except Course.DoesNotExist:
            raise Http404("Encontramos um erro")
        if request.method == 'POST':
            form = InscricaoCurso(request.POST)

            if form.is_valid():
                print('antes: '+str(c)+'-'+str(c.students.all()))
                print(request.user)
                c.students.add(request.user)
                c.save()
                print('depois: '+str(c)+'-'+str(c.students.all()))
                return redirect('/genus/'+curso_slug+'/')
            else:
                #handle invalid form
                return redirect('/genus/'+curso_slug+'/resumo/')
        else:
            print(request.user)
            print(c.owner)
            form = None
            if ((not request.user in c.students.all()) and (request.user != c.owner)):
                form = InscricaoCurso(initial={'course':c})
            return render(request, 'resumoCurso.html', {'curso':c, 'form': form})
    else:
        return redirect('/')

def curso(request, curso_slug):
    if request.user.is_authenticated:
        dono=False
        try:
            c= Course.objects.get(slug=curso_slug)
        except Course.DoesNotExist:
            raise Http404("Encontramos um erro")
        if(request.user==c.owner):
            dono=True
        return render(request, 'muralCurso.html', {'curso':c, 'dono': dono})
    else:
        return redirect('/')

def modulos(request, curso_slug):
    if request.user.is_authenticated:
        dono=False
        try:
            c= Course.objects.get(slug=curso_slug)
            m= Module.objects.filter(course=c)
            m= m.filter( Q(not_instance_of=Activity) & Q(not_instance_of=Post))
            ap = Module.objects.filter(Q(instance_of=Activity) | Q(instance_of=Post))
            ap= ap.filter(Q(Activity___module__in = m) | Q(Post___module__in = m))
        except Course.DoesNotExist:
            raise Http404("Encontramos um erro")
        except Module.DoesNotExist:
            m=None
        except Activity.DoesNotExist:
            a=None

        if(request.user==c.owner):
            dono=True

        return render(request, 'modulosCurso.html', {'curso':c, 'dono': dono, 'modulos': m, 'atividades_posts': ap})
    else:
        return redirect('/')

def criar_modulo(request, curso_slug):
    if request.user.is_authenticated:
        try:
            c= Course.objects.get(slug=curso_slug)
        except Course.DoesNotExist:
            raise Http404("Encontramos um erro")
        if(request.user==c.owner):
            if request.method == 'POST':
                form = CreateModuleForm(request.POST)
                if form.is_valid():
                    record = form.save(commit=False)
                    record.course=c
                    form.save()    
                    return redirect('/genus/'+curso_slug+'/modulos/')
            else:
                form = CreateModuleForm()
                return render(request, 'createModule.html', {'form': form})
        else:
            print("Você não tem permissão para criar um módulo nesse curso")
            return redirect('/genus/'+curso_slug)
    else:
        return redirect('/')


def exibir_modulo(request, curso_slug, modulo_id):
    if request.user.is_authenticated:
        dono=False

        try:
            c= Course.objects.get(slug=curso_slug)
            m= Module.objects.get(pk=modulo_id)
            ap = Module.objects.filter(Q(Activity___module = m) | Q(Post___module = m))
        except Course.DoesNotExist:
            raise Http404("Ops, esse curso não existe")
        except Course.DoesNotExist:
            raise Http404("Ops, esse módulo não existe")
        
        if request.user==c.owner:
            dono=True
        return render(request, 'modulo.html', {'curso':c, 'dono': dono, 'modulo': m, 'atividades_posts':ap})

    else:
        return redirect('/')

def criar_atividade(request, curso_slug, modulo_id):
    dono=False
    try:
        c= Course.objects.get(slug=curso_slug)
        m= Module.objects.get(pk=modulo_id)
    except Course.DoesNotExist:
        raise Http404("Ops, esse curso não existe")
    except Course.DoesNotExist:
        raise Http404("Ops, esse módulo não existe")
    if(request.user==c.owner):
            dono=True
    if request.user.is_authenticated:
        if dono:
            if request.method == 'POST':
                form = CreateActivityForm(request.POST)
                if form.is_valid():
                    record = form.save(commit=False)
                    record.course=c
                    record.module=m
                    form.save()

                    return redirect('/genus/'+curso_slug+'/'+str(modulo_id)+'/')
            else:

                form = CreateActivityForm()
            return render(request, 'createActivity.html', {'form': form})
        else:
            print("opaopa")
            return redirect('/genus/inicio/')
    else:
        return redirect('/')

def criar_post(request, curso_slug, modulo_id):
    dono=False
    try:
        c= Course.objects.get(slug=curso_slug)
        m= Module.objects.get(pk=modulo_id)
    except Course.DoesNotExist:
        raise Http404("Ops, esse curso não existe")
    except Course.DoesNotExist:
        raise Http404("Ops, esse módulo não existe")
    if(request.user==c.owner):
            dono=True
    if request.user.is_authenticated:
        if dono:
            if request.method == 'POST':
                form = CreatePostForm(request.POST)
                if form.is_valid():
                    record = form.save(commit=False)
                    record.course=c
                    record.module=m
                    form.save()
                    # owner = request.user
                    # subject = form.cleaned_data.get('subject')
                    # title = form.cleaned_data.get('title')
                    # overview = form.cleaned_data.get('overview')
                    # slug = slugify(form.cleaned_data.get('title'))

                    # curso = Course(owner=owner, subject=subject, title=title, overview=overview, slug=slug)
                    # curso.save()
                    
                    return redirect('/genus/'+curso_slug+'/'+str(modulo_id)+'/')
            else:

                form = CreatePostForm()
            return render(request, 'createPost.html', {'form': form})
        else:
            print("opaopa")
            return redirect('/genus/inicio/')

def exibir_atividade_post(request, curso_slug, modulo_id, atividade_post_id):
    if request.user.is_authenticated:
        dono=False
        try:
            c = Course.objects.get(slug=curso_slug)
            m = Module.objects.get(pk=modulo_id)
            ap = Module.objects.get(Q(Activity___pk = atividade_post_id) | Q(Post___pk = atividade_post_id))
            content = Content.objects.filter(module=ap)
            content_modulo=[]
            content_estudantes=[]
            own_resposta=[]
            for cont in content:
                if cont.item.owner==c.owner:
                    content_modulo.append(cont)
                else:
                    content_estudantes.append(cont)
                    if cont.item.owner==request.user:
                        own_resposta.append(cont)

        except Course.DoesNotExist:
            raise Http404("Ops, esse curso não existe")
        except Module.DoesNotExist:
            raise Http404("Ops, esse módulo ou conteudo não existe")
        
        if request.user==c.owner:
            dono=True
        return render(request, 'atividade.html', {'curso':c, 'dono': dono, 'modulo': m, 'atividade_post': ap, 'contents_modulo': content_modulo, 'respostas_estudantes':content_estudantes, 'respostas': own_resposta})

    else:
        return redirect('/')

tipo_form = {
  "2": AddTextForm,
  "3": AddImageForm,
  "4": AddVideoForm,
  "5": AddFileForm,
}

def adicionar_arquivo(request, curso_slug, modulo_id, atividade_post_id):
    if request.user.is_authenticated:
        dono=False
        try:
            c = Course.objects.get(slug=curso_slug)
        except Course.DoesNotExist:
            raise Http404("Ops, esse curso não existe")

        try:
            m = Module.objects.get(pk=modulo_id)
        except Module.DoesNotExist:
            raise Http404("Ops, esse módulo ou conteudo não existe")

        try:
            ap = Module.objects.get(Q(Activity___pk = atividade_post_id) | Q(Post___pk = atividade_post_id))
        except Module.DoesNotExist:
            raise Http404("Ops, esse módulo ou conteudo não existe")
        
        if request.method == 'POST':
            form1 = EscolhaTipo(request.POST)

            if form1.is_valid():
                
                if('arquivo' in request.POST):
                    tipo = form1.cleaned_data.get('escolha')
                    form2=tipo_form[tipo](request.POST, request.FILES)

                    if form2.is_valid():
                        record = form2.save(commit=False)
                        record.owner=request.user
                        form2.save()

                        Content.objects.create(module=ap,item=record)
                        return redirect('/genus/'+curso_slug+'/'+str(modulo_id)+'/'+str(atividade_post_id)+'/')
                    else:
                        # handle invalid form
                        return redirect('/genus/'+curso_slug+'/'+str(modulo_id)+'/'+str(atividade_post_id)+'/')

                else:
                    tipo = form1.cleaned_data.get('escolha')
                    form2=tipo_form[tipo]()
                    return render(request, 'addArquivo2.html', {'form1': form1, 'form2': form2})
            else:
                # handle invalid form
                return redirect('/genus/'+curso_slug+'/'+str(modulo_id)+'/'+str(atividade_post_id)+'/')

        else:
            form1 = EscolhaTipo()
            return render(request, 'addArquivo2.html', {'form1': form1, 'form2': None})
    else:
        return redirect('/')

def adicionar_comentario(request, curso_slug, modulo_id, atividade_post_id):
    try:
        c= Course.objects.get(slug=curso_slug)
        m= Module.objects.get(pk=modulo_id)
        p= Module.objects.get(Q(Activity___pk = atividade_post_id) | Q(Post___pk = atividade_post_id))
        # p= Post.objects.get(pk=atividade_post_id)
        #a= Comment.author = request.user
    except Course.DoesNotExist:
        raise Http404("Ops, esse curso não existe")
    except Course.DoesNotExist:
        raise Http404("Ops, esse módulo não existe")
    
    if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    record = form.save(commit=False)
                    record.author = request.user
                    record.course=c
                    record.module=m
                    record.post=p 
                    form.save()
                    return redirect('/genus/'+curso_slug+'/'+str(modulo_id)+'/'+str(atividade_post_id))
    else:
        form = CommentForm()    
        return render(request, 'addComentario.html',{'form': form, 'atividade_post': p,})


# def criar_post(request, curso_slug, modulo_id):
#     if request.user.is_authenticated:
#         dono=False
        
#     else:
#         return redirect('/')


# class ContentCreateUpdateView(TemplateResponseMixin, View):
#     module = None
#     model = None
#     obj = None
#     template_name = 'courses/manage/content/form.html'
    
#     def get_model(self, model_name):
#         if model_name in ['text', 'video', 'image', 'file']:
#             return apps.get_model(app_label='courses',model_name=model_name)
#         return None
    
#     def get_form(self, model, *args, **kwargs):
#         Form = modelform_factory(model, exclude=['owner','order','created','updated'])

#         return Form(*args, **kwargs)
    
#     def dispatch(self, request, module_id, model_name, id=None):
#         self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
#         self.model = self.get_model(model_name)
        
#         if id:
#             self.obj = get_object_or_404(self.model, id=id,owner=request.user)
#         return super(ContentCreateUpdateView,self).dispatch(request, module_id, model_name, id)
    
#     def get(self, request, module_id, model_name, id=None):
#         form = self.get_form(self.model, instance=self.obj)
#         return self.render_to_response({'form': form,'object': self.obj})

#     def post(self, request, module_id, model_name, id=None):
#         form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.owner = request.user
#             obj.save()
#             if not id:
#                 # new content
#                 Content.objects.create(module=self.module,item=obj)
#             return redirect('module_content_list', self.module.id)
#         return self.render_to_response({'form': form, 'object': self.obj})

def teste(request):
    c = Course.objects.get(slug='teste')
    print(c.students)
    return redirect('/')

def exibir_alunos(request, curso_slug):
    if request.user.is_authenticated:
        try:
            c = Course.objects.get(slug=curso_slug)
        except Course.DoesNotExist:
            raise Http404("Ops, esse curso não existe")
        alunos=c.students.all()
        return render(request, 'alunos.html', {'curso': c, 'alunos': alunos})

    else:
        return redirect('/')

def exibir_respostas(request, curso_slug, modulo_id, atividade_post_id):
    if request.user.is_authenticated:
        try:
            c = Course.objects.get(slug=curso_slug)
            m = Module.objects.get(pk=modulo_id)
            ap = Module.objects.get(Q(Activity___pk = atividade_post_id) | Q(Post___pk = atividade_post_id))
        except Course.DoesNotExist:
            raise Http404("Ops, esse curso não existe")
        except Module.DoesNotExist:
            raise Http404("Ops, esse módulo ou conteudo não existe")

        alunos=c.students.all()
        return render(request, 'respostasAlunos.html', {'curso':c,'modulo': m,'atividade_post': ap,'alunos': alunos, 'resposta': None})
    else:
        return redirect('/')

def exibir_resposta_de_aluno(request, curso_slug, modulo_id, atividade_post_id, aluno):
    if request.user.is_authenticated:
        try:
            c = Course.objects.get(slug=curso_slug)
            m = Module.objects.get(pk=modulo_id)
            ap = Module.objects.get(Q(Activity___pk = atividade_post_id) | Q(Post___pk = atividade_post_id))
            content = Content.objects.filter(module=ap)
            resposta=[]
            for cont in content:
                if cont.item.owner.username==aluno:
                    print('entrei')
                    resposta.append(cont)

        except Course.DoesNotExist:
            raise Http404("Ops, esse curso não existe")
        except Module.DoesNotExist:
            raise Http404("Ops, esse módulo ou conteudo não existe")

        alunos=c.students.all()
        print(content)
        print(resposta)
        print(cont.item.owner)
        print(aluno)
        return render(request, 'respostasAlunos.html', {'curso':c,'modulo': m,'atividade_post': ap,'alunos': alunos, 'resposta': resposta, 'aluno': aluno})
    else:
        return redirect('/')