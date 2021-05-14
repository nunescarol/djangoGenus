from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from cursos.models import Course

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ("username", "first_name","last_name","email", )
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        user.first_name = first_name
        user.last_name = last_name
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class InscricaoCurso(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)