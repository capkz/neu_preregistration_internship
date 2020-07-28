from django.shortcuts import render
from django.utils import timezone
from .models import ogrenci
from .forms import ogrenci_formu

def ogrenci_bilgileri(request):
    return render(request, 'onkayit/ogrenci_bilgileri.html')

def test(request):
    ogrenci_form = ogrenci_formu()
    ogrenciler = ogrenci.objects.all().order_by('id')
    if ogrenci_form.is_valid():
        form.save()
        return render(request, 'onkayit/test.html', {'ogrenci_formu': ogrenci_form})
    else:
        print("ERROR")
    return render(request, 'onkayit/test.html', {'ogrenci_formu': ogrenci_form})

    #'ogrenciler':ogrenciler