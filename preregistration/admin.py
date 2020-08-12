from django.contrib import admin
from .models import student,disposable,disposable_parents,disposable_transportation

admin.site.register(student)
admin.site.register(disposable)
admin.site.register(disposable_parents)
admin.site.register(disposable_transportation)