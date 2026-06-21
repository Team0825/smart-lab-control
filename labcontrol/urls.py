from django.contrib import admin
from django.urls import path
from monitoring import views

urlpatterns = [

    path('version/', views.app_version),

    path("login-api/", views.login_api),

    path('students/', views.student_list),
    path('students/add/', views.add_student),
    path('students/edit/<int:id>', views.edit_student),
    path('students/delete/<int:id>/', views.delete_student),

    path('create-session/', views.create_session),
    path('check-session/', views.check_session),
    path('sessions/', views.session_list),
    path('sessions/end/<int:id>/', views.end_session),

    path('attendance/', views.attendance_report),

    path("student-panel/", views.student_panel, name="student_panel"),

    path("send-notice/", views.send_notice),
    path("sent-notice/", views.send_notice),
    path("get-notice/", views.get_notice),

    path('admin/', admin.site.urls),

    path('', views.student_login),

    path('api/report/', views.report_pc),

    path('admin-panel/', views.admin_panel),
    path('dashboard/', views.admin_dashboard),
    path('control/', views.admin_dashboard),

    path('logout/', views.admin_logout),

    path('set-command/', views.set_command),
    path('get-command/', views.get_command),

    path('update-settings/', views.update_settings),
    path('get-settings/', views.get_settings),

    path('remove-site/', views.remove_site),
    path('block-site/', views.block_site),
    path('unblock-site/', views.unblock_site),
]