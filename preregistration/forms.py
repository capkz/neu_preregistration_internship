from django import forms
from .models import student

class student_information_form(forms.ModelForm):
    class Meta:
        model = student
        fields = ('name','surname','id_no','sex','birth_place',
        'birth_date','nationality','blood_type','adress','area','phone_number',
        'home_phone_number','general_information','medical_information','foreign_language',
        'registration_type','previous_school','scholarship',)