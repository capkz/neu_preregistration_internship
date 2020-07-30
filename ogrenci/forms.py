from django import forms
from onkayit.models import ogrenci

class ogrenci_arama(forms.ModelForm):
    class Meta:
        model = ogrenci
        fields = ('id',)