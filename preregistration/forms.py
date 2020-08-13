from django import forms
from .models import student, parent, sibling, transportation, pickup_backup

class student_form(forms.ModelForm):
    class Meta:
        model = student
        fields = '__all__'

class parent_form(forms.ModelForm):
    class Meta:
        model = parent
        fields = '__all__'

class sibling_form(forms.ModelForm):
    class Meta:
        model = sibling
        fields = '__all__'
        
class transportation_form(forms.ModelForm):
    class Meta:
        model = transportation
        fields = '__all__'
        
class pickup_backup_form(forms.ModelForm):
    class Meta:
        model = pickup_backup
        fields = '__all__'      