from django.conf import settings
from django.db import models
from django.utils import timezone

sexes = [('M','Male'),('K','Female')]
blood_types = [('0-','0-'),('0+','0+'),('A-','A-'),('A+','A+'),('B-','B-'),('B+','B+'),('AB-','AB-'),('AB+','AB+')]
registration_types = [('internet','Internet'),('email','Email'),('telephone','Telephone')]
student_stasuses = [('active','Active'),('passive','Passive')]
educational_stasuses = [('primary','Primary'),('secondary','Secondary'),('university','University'),('none','None')]
scholarships = [('0','0'),('25','25'),('50','50'),('75','75'),('100','100')]
marital_statuses = [('together','Together'),('divorced','Divorced')]
states = [('alive','Alive'),('deceased','Deceased')]
relations = [('mom','Mom'),('dad','Dad'),('sibling','Sibling')]
schools = [('none','None'),('neu primary','Near East Primary School'),('neu college','Near East College'),('other','Other')]
ways = [('to school','To School'),('fromschool','From School'),('both ways','Both Ways')]
areas = [('gazimağusa','Gazimağusa'),('güzelyurt','Güzelyurt'),('girne','Girne'),('lefkoşa','Lefkoşa'),('lefke','Lefke')]

class student(models.Model):
    photo = models.ImageField()
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
    address = models.TextField()
    area = models.CharField(max_length=20, choices=areas)
    phone_number = models.CharField(max_length=15)
    home_phone_number = models.CharField(max_length=15)
    general_information = models.TextField()
    medical_information = models.TextField()
    registration_date = models.DateTimeField(default=timezone.now())
    foreign_language = models.CharField(max_length=15) 
    registration_type = models.CharField(max_length=10, choices=registration_types)
    previous_school = models.CharField(max_length=30)
    scholarship = models.CharField(max_length=10, choices=scholarships)
    sibling_discount = models.BooleanField()
    password = models.CharField(max_length=20)

    parents_marital_status = models.CharField(max_length=10, choices=marital_statuses)
    is_dad_married = models.BooleanField()
    is_mother_married = models.BooleanField()
    mother_state = models.CharField(max_length=10, choices=states)
    dad_state = models.CharField(max_length=10, choices=states)

    def __str__(self):
        return self.name+" "+self.surname

class parent(models.Model):
    related_student = models.ForeignKey('student', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    relation = models.CharField(max_length=8,choices=relations)
    id_no = models.CharField(max_length=20) 
    nationality = models.CharField(max_length=20)
    is_guardian = models.BooleanField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    home_phone_number = models.CharField(max_length=15)
    work_phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length = 50) 
    job = models.CharField(max_length=40)
    workplace_name = models.CharField(max_length= 40)
    education_status = models.CharField(max_length=20, choices=educational_stasuses)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.related_student

class sibling(models.Model):
    related_student = models.ForeignKey('student', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    registered_school = models.CharField(max_length=20,choices=schools)
    registered_school = models.CharField(max_length=20,choices=schools)

    def __str__(self):
        return self.related_student

class transportation(models.Model):
    related_student = models.ForeignKey('student', on_delete=models.CASCADE)
    is_transportation = models.BooleanField()
    which_way = models.CharField(max_length=15, choices=ways)
    
    pick_up_area = models.CharField(max_length=20,choices=areas)
    pick_up_address = models.TextField()

    drop_off_area = models.CharField(max_length=20,choices=areas)
    drop_off_address = models.TextField()

    def __str__(self):
        return self.related_student

class pickup_backup(models.Model):
    related_student = models.ForeignKey('student', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    relation = models.CharField(max_length=15)

    def __str__(self):
        return self.related_student

class disposable(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length = 50) 
    birth_date = models.DateField()
    
class disposable_parents(models.Model):
    related = models.ForeignKey('disposable', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birth_date = models.DateField()

class disposable_transportation(models.Model):
    related = models.ForeignKey('disposable', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=30)
    pickup_date = models.DateField()