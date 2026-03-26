from django.db import models

from django.db import models

class PC(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.CharField(max_length=50, default="0.0.0.0")
    status = models.CharField(max_length=20, default="offline")

    def __str__(self):
        return self.name
    
    
class AllowedWebsite(models.Model):
    url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.url
    
class Student(models.Model):
    registration_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.registration_number


class LoginRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pc_name = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=20)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.pc_name}"
    
class BlockedWebsite(models.Model):
    url = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.url