from django.contrib import admin
from .models import (
    PC,
    AllowedWebsite,
    BlockedWebsite,
    Student,
    Session,
    LoginRecord,
    Command,
    Notice
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
        "login_time",
        "logout_time"
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
        "current_student",
        "current_session",
        "last_seen"
    )

    search_fields = (
        "name",
        "ip"
    )


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = (
        "pc_name",
        "command",
        "executed",
        "created_at"
    )

    list_filter = (
        "executed",
    )

    search_fields = (
        "pc_name",
        "command"
    )


admin.site.register(AllowedWebsite)
admin.site.register(BlockedWebsite)
admin.site.register(Notice)