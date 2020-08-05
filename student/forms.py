from django import forms
from preregistration.models import student

class student_search(forms.ModelForm):
    class Meta:
        model = student
        fields = ('id',)