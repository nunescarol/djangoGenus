from django import forms
from django.forms import ModelForm

from .models import Subject, Module, Activity, Post, Content, Image, Text, File, Video, Comment

class CreateCourseForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.order_by('title'),label="Área",widget=forms.Select(attrs={'class':'testclass'}))
    title = forms.CharField(max_length=100, label="Nome")
    overview = forms.CharField(widget=forms.Textarea, label="Descrição")

class CreateModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']

class CreateActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description']

class CreatePostForm(ModelForm):
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

# class CreateActivityAdminForm(ModelForm):
#     class Meta:
#         model = Activity
#         fields = ['title', 'description', 'course']

