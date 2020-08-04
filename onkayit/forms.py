from django import forms
from .models import ogrenci

class ogrenci_formu(forms.ModelForm):
    class Meta:
        model = ogrenci
        fields = ('ad','soyad','kimlik_no','cinsiyet','doğum_yeri',
        'doğum_tarihi','uyruk','kan_grubu','adres','bölge','cep_tel',
        'ev_tel','genel_bilgi','sağlık_bilgisi','yabancı_dil',
        'kayıt_kabul','onceki_okul','burs',)