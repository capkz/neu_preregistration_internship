from django.contrib import admin
from .models import student,transportation,sibling,parent,pickup_backup

admin.site.register(student)
admin.site.register(transportation)
admin.site.register(sibling)
admin.site.register(parent)
admin.site.register(pickup_backup)