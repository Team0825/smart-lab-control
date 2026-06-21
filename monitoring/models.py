from django.db import models
from django.utils import timezone


class Student(models.Model):
    registration_number = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.registration_number} - {self.name}"


class Session(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    active = models.BooleanField(default=True)

    def is_active(self):
        end_time = self.start_time + timezone.timedelta(minutes=self.duration)
        return timezone.now() <= end_time and self.active

    def __str__(self):
        return f"{self.title} ({self.code})"


class PC(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.CharField(max_length=50, default="0.0.0.0")
    status = models.CharField(max_length=20, default="offline")
    last_seen = models.DateTimeField(default=timezone.now)

    # Phase 5
    current_student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    current_session = models.ForeignKey(
        Session,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

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


class LoginRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    pc_name = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=20)

    login_time = models.DateTimeField(auto_now_add=True)

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.pc_name}"


# =====================================
# Phase 5 Command Storage
# =====================================
class Command(models.Model):

    pc_name = models.CharField(max_length=100)

    command = models.CharField(max_length=50)

    executed = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.pc_name} - {self.command}"
    
class Notice(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]