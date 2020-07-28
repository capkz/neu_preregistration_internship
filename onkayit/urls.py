from django.urls import path
from . import views

urlpatterns = [
    path('',views.test, name='test'),
    path('onkayit/ogrenci_bilgileri', views.ogrenci_bilgileri, name='ogrenci_bilgileri'),
]