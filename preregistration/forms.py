from django import forms
from .models import student, parent, sibling, transportation, pickup_backup
from client_side_image_cropping import ClientsideCroppingWidget
from django.conf import settings

class student_form(forms.ModelForm):
    class Meta:
        model = student
        exclude = ["user","registration_date"]
        widgets = {
            'photo': ClientsideCroppingWidget(
                width=600,
                height=600,
                preview_width=0,
                preview_height=0,     
            )
        }
        input_formats = {
            'input_formats': settings.DATE_INPUT_FORMATS
        }
        
class student_search(forms.ModelForm):
    class Meta:
        model = student
        fields = ('id',)
        
class parent_form(forms.ModelForm):
    class Meta:
        model = parent
        fields = '__all__'
        exclude = ["relation","related_student"]

class sibling_form(forms.ModelForm):
    class Meta:
        model = sibling
        fields = '__all__'
        exclude = ["related_student","id"]
        
class transportation_form(forms.ModelForm):
    class Meta:
        model = transportation
        fields = '__all__'
        exclude = ["related_student"]
        
class pickup_backup_form(forms.ModelForm):
    class Meta:
        model = pickup_backup
        fields = '__all__'      
        exclude = ["related_student"]