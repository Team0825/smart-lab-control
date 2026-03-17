from django.contrib import admin
from .models import Student, LoginRecord, AllowedWebsite

admin.site.register(AllowedWebsite)
admin.site.register(Student)
admin.site.register(LoginRecord)