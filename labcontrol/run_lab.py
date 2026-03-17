import os
import socket
import subprocess
import time
import webbrowser

print("\n====================================")
print(" SMART LAB CONTROL SERVER STARTING ")
print("====================================\n")

# Folder where EXE is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Move one level up -> labcontrol folder
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

os.chdir(PROJECT_DIR)

print("Project directory:", PROJECT_DIR)

# Check manage.py
if not os.path.exists("manage.py"):
    print("ERROR: manage.py not found!")
    input("Press Enter to exit...")
    exit()

# Detect local IP
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
except:
    ip = "127.0.0.1"

port = "8000"

print("\nStudent Login:")
print(f"http://{ip}:{port}")

print("\nMobile Control:")
print(f"http://{ip}:{port}/control/\n")

print("Starting Django server...")

server = subprocess.Popen(
    ["python", "manage.py", "runserver", "0.0.0.0:8000"]
)

time.sleep(5)

webbrowser.open(f"http://{ip}:{port}")

server.wait()