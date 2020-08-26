from django.contrib import admin
from .models import student,transportation,sibling,parent,pickup_backup
from django.contrib.auth.models import Permission

admin.site.register(Permission)
admin.site.register(student)
admin.site.register(transportation)
admin.site.register(sibling)
admin.site.register(parent)
admin.site.register(pickup_backup)