from django.contrib import admin
from django.urls import path
from monitoring import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.student_login),

    path('api/report/', views.report_pc),

    path('admin-panel/', views.admin_panel),
    path('dashboard/', views.admin_dashboard),

    path('logout/', views.admin_logout),

    path('control/', views.admin_dashboard),

    path('set-command/', views.set_command),
    path('get-command/', views.get_command),

    path('update-settings/', views.update_settings),
    path('get-settings/', views.get_settings),

    path('remove-site/', views.remove_site),
    path('block-site/', views.block_site),
    path('unblock-site/', views.unblock_site),
]