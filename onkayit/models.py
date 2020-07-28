from django.conf import settings
from django.db import models
from django.utils import timezone

cinsiyetler = [('E','Erkek'),('K','Kadın'),('D','Diğer')]
kan_grupları = [('0-','0-'),('0+','0+'),('A-','A-'),('A+','A+'),('B-','B-'),('B+','B+'),('AB-','AB-'),('AB+','AB+')]
kayit_sekilleri = [('Internet','İnternet'),('Email','Email')]


class ogrenci(models.Model):
    kullanıcı = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.CharField(max_length=30)
    soyad = models.CharField(max_length=(30))
    kimlik_no = models.CharField(max_length=20) 
    cinsiyet = models.CharField(max_length=5, choices=cinsiyetler)
    doğum_yeri = models.CharField(max_length=15)
    doğum_tarihi = models.DateField()
    uyruk = models.CharField(max_length=20)
    kan_grubu = models.CharField(max_length=3, choices=kan_grupları)
    adres = models.TextField()
    bölge = models.CharField(max_length=20)
    cep_tel = models.CharField(max_length=15)
    ev_tel = models.CharField(max_length=15)
    genel_bilgi = models.TextField()
    sağlik_bilgisi = models.TextField()
    kayıt_tarihi = models.DateTimeField(default=timezone.now())
    yabancı_dil = models.CharField(max_length=15) 
    kayıt_kabul = models.CharField(max_length=10, choices=kayit_sekilleri)
    onceki_okul = models.CharField(max_length=30)
    burs = models.CharField(max_length=10)


    class Meta:
        verbose_name_plural = "öğrenciler"

    def __str__(self):
        return self.ad+" "+self.soyad
    