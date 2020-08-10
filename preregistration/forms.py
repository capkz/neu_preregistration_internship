from django import forms
from .models import student, parents, siblings, transportation, pickup_backup, disposable

class student_information_form(forms.ModelForm):
    class Meta:
        model = student
        fields = '__all__'

class family_information_form(forms.ModelForm):
    class Meta:
        model = parents
        fields = '__all__'

class disposable_form(forms.ModelForm):
    class Meta:
        model = disposable
        fields = '__all__'