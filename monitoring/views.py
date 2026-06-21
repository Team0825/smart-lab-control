from django.shortcuts import render, redirect
from .models import (Student,
                     LoginRecord,
                     AllowedWebsite,
                     BlockedWebsite,
                     PC,
                     Session,
                     Command
                     )
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import random
import json
import socket
import qrcode
import base64
from io import BytesIO


# ==========================
# SESSATION CREATION
# ==========================


@staff_member_required
def create_session(request):

    if request.method == "POST":

        title = request.POST.get("title")
        duration = int(request.POST.get("duration"))

        code = str(random.randint(100000,999999))

        Session.objects.create(
            title=title,
            duration=duration,
            code=code
        )

        return render(request,"create_session.html",{"code":code})

    return render(request,"create_session.html")
# ==========================
# SESSATION
# ==========================


def check_session(request):

    try:

        record = LoginRecord.objects.latest('login_time')

        session = record.session

        if not session.is_active():

            if record.logout_time is None:
                record.logout_time = timezone.now()
                record.save()

            return JsonResponse({
                "active": False
            })

        return JsonResponse({
            "active": True
        })

    except:
        return JsonResponse({
            "active": False
        })
        
        
   
def session_list(request):
    
    sessions = Session.objects.all().order_by("-start_time")
    return render(
        request,
        "session_list.html",
        {
            "sessions": sessions
        }
    )    
    
# ==========================
# Session list
# ==========================
@staff_member_required
def end_session(request, id):
    try:
        session = Session.objects.get(id=id)
        session.active = False
        session.save()
    except:
        pass
    return redirect("/sessions/")

def attendance_report(request):
    records = LoginRecord.objects.select_related(
        "student",
        "session"
    ).order_by("-login_time")
    return render(
        request,
        "attendance.html",
        {
            "records": records
        }
    )    
# ==========================
# STUDENT MANAGEMENT
# ==========================

def student_list(request):

    students = Student.objects.all().order_by("registration_number")

    return render(request, "students.html", {
        "students": students
    })


def add_student(request):

    if request.method == "POST":

        Student.objects.create(
            registration_number=request.POST.get("registration_number"),
            name=request.POST.get("name"),
            department=request.POST.get("department"),
            semester=request.POST.get("semester")
        )

        return redirect("/students/")

    return render(request, "add_student.html")


def edit_student(request, id):

    student = Student.objects.get(id=id)

    if request.method == "POST":

        student.registration_number = request.POST.get("registration_number")
        student.name = request.POST.get("name")
        student.department = request.POST.get("department")
        student.semester = request.POST.get("semester")

        student.save()

        return redirect("/students/")

    return render(request, "edit_student.html", {
        "student": student
    })


def delete_student(request, id):

    Student.objects.get(id=id).delete()

    return redirect("/students/")    
# ==========================
# STUDENT LOGIN 
# ==========================

def student_login(request):

    if request.method == "POST":

        reg = request.POST.get("registration", "").strip()
        session_code = request.POST.get("session_code", "").strip()

        if not reg or not session_code:
            return render(
                request,
                "login.html",
                {
                    "error": "Registration number and session code are required"
                }
            )

        try:
            student = Student.objects.get(
                registration_number__iexact=reg
            )
        except Student.DoesNotExist:
            return render(
                request,
                "login.html",
                {
                    "error": "Invalid registration number"
                }
            )

        try:
            session = Session.objects.get(
                code=session_code
            )
        except Session.DoesNotExist:
            return render(
                request,
                "login.html",
                {
                    "error": "Invalid session code"
                }
            )

        try:
            # Session active check
            if not session.is_active():
                return render(
                    request,
                    "login.html",
                    {
                        "error": "Session expired or invalid"
                    }
                )

            # Prevent multiple login
            already_logged = LoginRecord.objects.filter(
                student=student,
                session=session
            ).exists()

            if already_logged:
                return render(
                    request,
                    "success.html",
                    {
                        "student": student
                    }
                )

            # PC details
            pc_name = socket.gethostname()
            ip_address = request.META.get("REMOTE_ADDR")

            # Update PC
            pc_obj, created = PC.objects.update_or_create(
                name=pc_name,
                defaults={
                    "ip": ip_address,
                    "status": "online",
                    "last_seen": timezone.now()
                }
            )

            pc_obj.current_student = student
            pc_obj.current_session = session
            pc_obj.save()

            # Save login record
            LoginRecord.objects.create(
                student=student,
                pc_name=pc_name,
                ip_address=ip_address,
                session=session
            )
            
            request.session["student_id"] = student.id
            request.session["session_id"] = session.id
            
            return redirect("/student-panel/")

        except Exception as e:
            return render(
                request,
                "login.html",
                {
                    "error": str(e)
                }
            )

              
    return render(request, "login.html")

# ==========================
# STUDENT Panel Request
# ==========================
def student_panel(request):

    student_id = request.session.get("student_id")
    session_id = request.session.get("session_id")

    if not student_id or not session_id:
        return redirect("/")

    try:
        student = Student.objects.get(id=student_id)
        session = Session.objects.get(id=session_id)

        end_time = session.start_time + timezone.timedelta(
            minutes=session.duration
        )

        remaining = int(
            (end_time - timezone.now()).total_seconds()
        )

        if remaining < 0:
            remaining = 0

        return render(
            request,
            "student_panel.html",
            {
                "student": student,
                "session": session,
                "remaining": remaining
            }
        )

    except:
        return redirect("/")

# ==========================
# ADMIN PANEL
# ==========================
def admin_panel(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    url = f"http://{ip}:8000/control/"

    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    return render(request, "admin_panel.html", {
        "qr": base64.b64encode(buffer.getvalue()).decode()
    })


@staff_member_required(login_url="/admin/login/")
def admin_dashboard(request):

    pcs = []

    all_pcs = PC.objects.all()

    for pc in all_pcs:

        try:
            login = LoginRecord.objects.filter(
                pc_name=pc.name
            ).latest("login_time")

            student_name = login.student.name

            if login.session:
                session_name = login.session.title
            else:
                session_name = "-"

        except:
            student_name = "-"
            session_name = "-"

        if timezone.now() - pc.last_seen > timedelta(seconds=15):
            status = "offline"
        else:
            status = "online"

        pcs.append({
            "name": pc.name,
            "ip": pc.ip,
            "status": status,
            "student": student_name,
            "session": session_name
        })

    allowed_sites = list(
        AllowedWebsite.objects.filter(active=True)
        .values_list("url", flat=True)
    )

    blocked_sites = list(
        BlockedWebsite.objects.filter(active=True)
        .values_list("url", flat=True)
    )

    return render(request, "dashboard.html", {
        "pcs": pcs,
        "allowed_sites": allowed_sites,
        "blocked_sites": blocked_sites
    })

# ==========================
# REPORT PC (FIXED)
# ==========================


@csrf_exempt
def report_pc(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            pc_name = data.get("pc_name")
            ip = data.get("ip")

            PC.objects.update_or_create(
                name=pc_name,
                defaults={
                    "ip": ip,
                    "status": "online",
                    "last_seen": timezone.now()
                }
            )

            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Use POST"})


# ==========================
# COMMAND
# ==========================
@csrf_exempt
def set_command(request):

    pc = request.GET.get("pc")
    cmd = request.GET.get("cmd")

    if not pc or not cmd:
        return JsonResponse(
            {"error": "Missing pc or cmd"},
            status=400
        )

    if pc == "ALL":
        all_pcs = PC.objects.all()
        for p in all_pcs:
            Command.objects.create(
                pc_name=p.name,
                command=cmd
            )
    else:
        Command.objects.create(
            pc_name=pc,
            command=cmd
        )

    return JsonResponse({"status": "ok"})

def get_command(request):
    pc = request.GET.get("pc")

    if not pc:
        return JsonResponse(
            {"error": "Missing pc"},
            status=400
        )

    command = (
        Command.objects
        .filter(pc_name=pc, executed=False)
        .order_by("created_at")
        .first()
    )

    if command is None:
        return JsonResponse({"command": "none"})

    command.executed = True
    command.save(update_fields=["executed"])

    return JsonResponse({"command": command.command})


# ==========================
# SETTINGS
# ==========================
@csrf_exempt
def update_settings(request):
    site = request.GET.get("site")

    if site:
        obj, _ = AllowedWebsite.objects.get_or_create(url=site)
        obj.active = True
        obj.save()

    return JsonResponse({"status": "ok"})


def get_settings(request):
    allowed = list(
        AllowedWebsite.objects.filter(active=True)
        .values_list("url", flat=True)
    )

    blocked = list(
        BlockedWebsite.objects.filter(active=True)
        .values_list("url", flat=True)
    )

    return JsonResponse({
        "allowed_sites": allowed,
        "blocked_sites": blocked
    })


@csrf_exempt
def remove_site(request):
    site = request.GET.get("site")
    AllowedWebsite.objects.filter(url=site).update(active=False)

    return JsonResponse({"status": "removed"})


@csrf_exempt
def block_site(request):
    site = request.GET.get("site")

    obj, _ = BlockedWebsite.objects.get_or_create(url=site)
    obj.active = True
    obj.save()

    return JsonResponse({"status": "blocked"})


@csrf_exempt
def unblock_site(request):
    site = request.GET.get("site")
    BlockedWebsite.objects.filter(url=site).update(active=False)

    return JsonResponse({"status": "ok"})


# ==========================
# LOGOUT
# ==========================
def admin_logout(request):
    logout(request)
    return redirect("/admin-panel/")
