from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from .models import Student, LoginRecord, AllowedWebsite, BlockedWebsite, PC
import json
import socket
import qrcode
import base64
from io import BytesIO

commands = {}
alerts = []


# ==========================
# STUDENT LOGIN
# ==========================

def student_login(request):

    if request.method == "POST":

        reg = request.POST.get("registration")

        try:
            student = Student.objects.get(registration_number=reg)

            LoginRecord.objects.create(
                student=student,
                pc_name=socket.gethostname(),
                ip_address=request.META.get("REMOTE_ADDR")
            )

            return render(request,"success.html",{"student":student})

        except:
            return render(request,"login.html",{"error":"Student not found"})

    return render(request,"login.html")


# ==========================
# ADMIN PANEL
# ==========================

def admin_panel(request):

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()

    url = f"http://{ip}:8000/control/"

    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    return render(request,"admin_panel.html",{
        "qr":base64.b64encode(buffer.getvalue()).decode()
    })


# ==========================
# DASHBOARD
# ==========================

@staff_member_required(login_url="/admin/login/")
def admin_dashboard(request):

    pcs = PC.objects.all()

    pc_list = []

    for pc in pcs:
        pc_list.append({
            "name": pc.name,
            "ip": pc.ip,
            "status": pc.status
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
        "pcs": pc_list,
        "allowed_sites": allowed_sites,
        "blocked_sites": blocked_sites
    })

# ==========================
# REGISTER PC
# ==========================

@csrf_exempt
def report_pc(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            pc_name = data.get("pc_name")
            ip = data.get("ip")
            status = data.get("status")

            if not pc_name:
                return JsonResponse({"error": "PC name missing"}, status=400)

            pc, created = PC.objects.update_or_create(
                name=pc_name,
                defaults={
                    "ip": ip or "0.0.0.0",
                    "status": status or "online"
                }
            )

            return JsonResponse({
                "status": "saved",
                "pc": pc.name
            })

        except Exception as e:
            print("🔥 ERROR IN REPORT:", str(e))   # IMPORTANT FOR DEBUG
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "POST required"})
# ==========================
# REGISTER PC
# ==========================

@csrf_exempt
def register_pc(request):

    if request.method == "POST":
        data = json.loads(request.body)
        
        PC.objects.create(
            name=data["name"],
            ip=data["ip"],
            status="online"
        )

    

    return JsonResponse({"status":"ok"})


# ==========================
# COMMAND
# ==========================

@csrf_exempt
def set_command(request):

    pc = request.GET.get("pc")
    cmd = request.GET.get("cmd")

    commands[pc] = cmd

    return JsonResponse({"status":"ok"})


def get_command(request):

    pc = request.GET.get("pc")

    return JsonResponse({"command":commands.get(pc,"none")})


# ==========================
# SETTINGS
# ==========================

@csrf_exempt
def update_settings(request):

    site = request.GET.get("site")

    if site:
        obj,created = AllowedWebsite.objects.get_or_create(url=site)
        obj.active=True
        obj.save()

    return JsonResponse({"status":"ok"})


def get_settings(request):

    allowed = list(
        AllowedWebsite.objects.filter(active=True)
        .values_list("url",flat=True)
    )

    blocked = list(
        BlockedWebsite.objects.filter(active=True)
        .values_list("url",flat=True)
    )

    return JsonResponse({
        "allowed_sites":allowed,
        "blocked_sites":blocked
    })


@csrf_exempt
def remove_site(request):

    site = request.GET.get("site")
    AllowedWebsite.objects.filter(url=site).update(active=False)

    return JsonResponse({"status":"removed"})


@csrf_exempt
def block_site(request):

    site = request.GET.get("site")

    obj,created = BlockedWebsite.objects.get_or_create(url=site)
    obj.active=True
    obj.save()

    return JsonResponse({"status":"blocked"})


@csrf_exempt
def unblock_site(request):

    site = request.GET.get("site")
    BlockedWebsite.objects.filter(url=site).update(active=False)

    return JsonResponse({"status":"ok"})


# ==========================
# LOGOUT
# ==========================

def admin_logout(request):
    logout(request)
    return redirect("/admin-panel/")