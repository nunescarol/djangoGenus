from django import forms
from django.forms import ModelForm

from .models import Subject, Module, Post, Content, Image, Text, File, Video, Comment, Grade, MensagemMural
from django.contrib.auth.models import User

class CreateCourseForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.order_by('title'),label="Área",widget=forms.Select(attrs={'class':'testclass'}))
    title = forms.CharField(max_length=100, label="Nome")
    overview = forms.CharField(widget=forms.Textarea, label="Descrição")

class CreateModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']


class CreatePostForm(ModelForm):
    title = forms.CharField(max_length= 100, label= "Título")
    description = forms.CharField(widget=forms.Textarea, label="Descrição")
    class Meta:
        model = Post
        fields = ['title', 'description']

class AddFileForm(ModelForm):
    class Meta:
        model = File
        exclude = ['owner', 'created', 'updated']

class AddImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ['owner', 'created', 'updated']

class AddTextForm(ModelForm):
    class Meta:
        model = Text
        exclude = ['owner', 'created', 'updated']

class AddVideoForm(ModelForm):
    class Meta:
        model = Video
        exclude = ['owner', 'created', 'updated']

STATUS_CHOICES = (
    (1, '------------'),
    (2, "Texto"),
    (3, "Imagem"),
    (4, "Vídeo"),
    (5, "Arquivo"),
)

class EscolhaTipo(forms.Form):
    escolha = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'onchange': "this.form.submit()"}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class GradeForm(forms.ModelForm):
    grade = forms.DecimalField(widget=forms.NumberInput(attrs={'min':"0",'max': "10", 'step':'0.05'}))

    class Meta:
        model = Grade
        fields = ('grade',)

class MensagemMuralForm(forms.ModelForm):
                       
    text = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'testclass', 'id':'message', 'name':'message','placeholder':'Deixe um recado para a turma...', 'onclick':'messageText()'}))

    class Meta:
        model = MensagemMural
        fields = ('text',)

class PerfilForm(forms.Form):
    username = forms.CharField(label='Nome de usuário', max_length=150,required=False)
    first_name = forms.CharField(label='Nome', max_length=150,required=False)
    last_name = forms.CharField(label='Sobrenome', max_length=150,required=False)
    # email = forms.EmailField(label='Email',required=False)

    class Meta:
        fields = ['username', 'first_name', 'last_name']

class PasswordChange(forms.Form):
    current_password = forms.CharField(max_length=128, label="Senha atual", widget=forms.PasswordInput)
    new_password1 = forms.CharField(max_length=128, label="Nova senha", widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=128, label="Confirmação da nova senha", widget=forms.PasswordInput)

    class Meta:
        fields = ['password']

class PasswordConfirm(forms.Form):
    current_password = forms.CharField(max_length=128, label="Confirme sua senha", widget=forms.PasswordInput)

    class Meta:
        fields = ['password']

# class CreateActivityAdminForm(ModelForm):
#     class Meta:
#         model = Activity
#         fields = ['title', 'description', 'course']

