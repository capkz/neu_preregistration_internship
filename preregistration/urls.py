from django.urls import path
from . import views

urlpatterns = [
    path('student_information/add',views.student_add, name='student_add'),
    path('student_information/edit/',views.student_edit, name='student_edit'),
    path('<int:pk>/<str:action>/<str:status>/',views.form_complete, name='form_complete'),
    #path('onkayit/ogrenci_bilgileri', views.ogrenci_bilgileri, name='ogrenci_bilgileri'),
]