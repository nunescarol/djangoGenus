from django import forms
from django.forms import ModelForm

from .models import Subject, Module

class CreateCourseForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.order_by('title'))
    title = forms.CharField(max_length=100)
    overview = forms.CharField(widget=forms.Textarea)

class CreateModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']

