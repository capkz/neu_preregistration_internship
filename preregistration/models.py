from django.conf import settings
from django.db import models
from django.utils import timezone

sexes = [('M','Male'),('K','Female'),('O','Other')]
blood_types = [('0-','0-'),('0+','0+'),('A-','A-'),('A+','A+'),('B-','B-'),('B+','B+'),('AB-','AB-'),('AB+','AB+')]
registration_types = [('internet','Internet'),('email','Email'),('telephone','Telephone')]
student_stasuses = [('active','Active'),('passive','Passive')]
educational_stasuses = [('primary','Primary'),('secondary','Secondary'),('university','University'),('none','None')]
scholarships = [('0','0'),('25','25'),('50','50'),('75','75'),('100','100')]

class student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_status = models.CharField(max_length=20, choices=student_stasuses)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=(30))
    id_no = models.CharField(max_length=20) 
    sex = models.CharField(max_length=5, choices=sexes)
    birth_place = models.CharField(max_length=15)    
    birth_date = models.DateField()
    nationality = models.CharField(max_length=20)
    blood_type = models.CharField(max_length=3, choices=blood_types)
    adress = models.TextField()
    area = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    home_phone_number = models.CharField(max_length=15)
    general_information = models.TextField()
    medical_information = models.TextField()
    registration_date = models.DateTimeField(default=timezone.now())
    foreign_language = models.CharField(max_length=15) 
    registration_type = models.CharField(max_length=10, choices=registration_types)
    previous_school = models.CharField(max_length=30)
    scholarship = models.CharField(max_length=10, choices=scholarships)

    # anne_adı = models.CharField(max_length=30)
    # anne_soyadı = models.CharField(max_length=(30))
    # anne_kimlik_no = models.CharField(max_length=20) 
    # anne_uyruk = models.CharField(max_length=20)
    # anne_adres = models.TextField()
    # anne_cep_tel = models.CharField(max_length=15)
    # anne_ev_tel = models.CharField(max_length=15)
    # anne_iş_tel = models.CharField(max_length=15)
    # anne_email = models.EmailField(max_length = 50) 
    # anne_meslek = models.CharField(max_length=40)
    # anne_eğitim = models.CharField(max_length=3, choices=egitim_durumlari)

    def __str__(self):
        return self.name+" "+self.surname

#class 