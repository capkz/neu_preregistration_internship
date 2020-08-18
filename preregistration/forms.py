from django import forms
from .models import student, parent, sibling, transportation, pickup_backup
from client_side_image_cropping import ClientsideCroppingWidget

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