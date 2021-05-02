from django import forms
from .models import Subject

class CreateCourseForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.order_by('title'))
    title = forms.CharField(max_length=100)
    overview = forms.CharField(widget=forms.Textarea)
