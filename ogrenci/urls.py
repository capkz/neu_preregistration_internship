from django.urls import path
from . import views

urlpatterns = [
    path('',views.ogrenci_listesi, name='ogrenci_listesi'),
]