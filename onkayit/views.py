from django.shortcuts import render
from django.utils import timezone
from .models import ogrenci
from .forms import ogrenci_formu
from django.shortcuts import redirect, get_object_or_404

def ogrenci_bilgileri(request):
    return render(request, 'onkayit/ogrenci_bilgileri.html', {'nbar': 'on_kayit'})


def test(request):
    ogrenci_form = ogrenci_formu(request.POST)
    #ogrenciler = ogrenci.objects.all().order_by('id')
    if ogrenci_form.is_valid():
        form = ogrenci_form.save(commit=False)
        form.kullanıcı = request.user
        form.kayıt_tarihi = timezone.now()
        form.save()
        return redirect('form_success', pk=form.pk)
    else:
        print("ERROR")
    return render(request, 'onkayit/test.html', {'ogrenci_formu': ogrenci_form})


def form_success(request,pk):
    ogrenci_detay = get_object_or_404(ogrenci, pk=pk)
    return render(request, 'onkayit/form_success.html', {'ogrenci':ogrenci_detay})

    #'ogrenciler':ogrenciler

