from django.shortcuts import render

def ogrenci_bilgileri(request):
    return render(request, 'onkayit/ogrenci_bilgileri.html')