from django.urls import path
from . import views

urlpatterns = [
    path('ogrenci_bilgileri/',views.test, name='on_kayit'),
    path('<int:pk>/success/',views.form_success, name='form_success'),
    #path('onkayit/ogrenci_bilgileri', views.ogrenci_bilgileri, name='ogrenci_bilgileri'),
]