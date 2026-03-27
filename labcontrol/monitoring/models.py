from django.db import models
from django.utils import timezone

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


class BlockedWebsite(models.Model):
    url = models.CharField(max_length=200)
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
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    pc_name = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=20)
    login_time = models.DateTimeField(auto_now_add=True)  

class PC(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.CharField(max_length=50, default="0.0.0.0")
    status = models.CharField(max_length=20, default="offline")
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Session(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()  # in minutes
    active = models.BooleanField(default=True)

    def is_active(self):
        from django.utils import timezone
        end_time = self.start_time + timezone.timedelta(minutes=self.duration)
        return timezone.now() <= end_time and self.active

    def __str__(self):
        return f"{self.title} ({self.code})"