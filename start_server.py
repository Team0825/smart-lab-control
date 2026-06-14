import os
import subprocess
import sys
import socket
import webbrowser
import time

print("\n====================================")
print(" SMART LAB CONTROL SERVER STARTING ")
print("====================================\n")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# ------------------------------
# DETECT NETWORK IP
# ------------------------------

def get_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()

    return ip

ip = get_ip()
port = "8000"

print("Server starting...\n")

print("Student Login:")
print(f"http://{ip}:{port}\n")

print("Mobile Control:")
print(f"http://{ip}:{port}/control/\n")

# ------------------------------
# START AGENT
# ------------------------------

agent_path = os.path.join(BASE_DIR, "..", "pc_client", "agent.py")

if os.path.exists(agent_path):

    print("Starting agent...\n")

    subprocess.Popen([sys.executable, agent_path])

else:

    print("Agent file not found\n")


# ------------------------------
# START DJANGO SERVER
# ------------------------------

server_process = subprocess.Popen(
    [sys.executable, "manage.py", "runserver", f"{ip}:{port}"]
)

time.sleep(3)

# ------------------------------
# OPEN LOGIN PAGE
# ------------------------------

webbrowser.open(f"http://{ip}:{port}")

server_process.wait()