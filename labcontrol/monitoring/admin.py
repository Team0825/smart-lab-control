from django.contrib import admin
from .models import (
    PC,
    AllowedWebsite,
    BlockedWebsite,
    Student,
    Session,
    LoginRecord
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number",
        "name",
        "department",
        "semester"
    )

    search_fields = (
        "registration_number",
        "name"
    )

    list_filter = (
        "department",
        "semester"
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "code",
        "duration",
        "active",
        "start_time"
    )

    search_fields = (
        "title",
        "code"
    )


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "session",
        "pc_name",
        "ip_address",
        "login_time"
    )

    search_fields = (
        "pc_name",
        "ip_address"
    )


@admin.register(PC)
class PCAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ip",
        "status",
        "last_seen"
    )


admin.site.register(AllowedWebsite)
admin.site.register(BlockedWebsite)