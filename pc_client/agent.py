import requests
import os
import time
import socket
import ctypes

# ===============================
# GET CURRENT PC IP
# ===============================
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


PC_NAME = get_ip()

# ===============================
# AUTO DETECT SERVER
# ===============================
def get_server():
    try:
        with open("server.txt", "r") as f:
            return f.read().strip()
    except:
        return None


SERVER = None

while SERVER is None:
    SERVER = get_server()
    print("Waiting for server...")
    time.sleep(2)

print("Connected to:", SERVER)

# ===============================
# INIT SERVER
# ===============================
SERVER = None

while SERVER is None:
    SERVER = get_server()
    if SERVER is None:
        print("❌ No server found... retrying in 5 sec")
        time.sleep(5)

print("🌐 Connected to server:", SERVER)

COMMAND_API = SERVER + "/get-command/"
SETTINGS_API = SERVER + "/get-settings/"
ALERT_API = SERVER + "/send-alert/"

print("🖥 Agent started for:", PC_NAME)


# ===============================
# HOSTS FILE PATH
# ===============================
HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"


# ===============================
# ALERT FUNCTION
# ===============================
def send_alert(message):

    try:
        requests.get(
            ALERT_API,
            params={
                "pc": PC_NAME,
                "msg": message
            },
            timeout=3
        )
    except:
        pass


# ===============================
# WARNING POPUP
# ===============================
def show_warning(msg):

    try:
        ctypes.windll.user32.MessageBoxW(
            0,
            msg,
            "Lab Warning",
            0x40 | 0x1
        )
    except:
        pass


# ===============================
# WEBSITE FILTER
# ===============================
def update_hosts(allowed_sites, blocked_sites):

    try:
        with open(HOSTS_FILE, "r") as f:
            lines = f.readlines()

        # Remove old rules
        lines = [l for l in lines if "#LAB_BLOCK" not in l]

        with open(HOSTS_FILE, "w") as f:

            for line in lines:
                f.write(line)

            # Always allow
            allow_list = allowed_sites + [
                "localhost",
                "127.0.0.1",
                PC_NAME,
                "accounts.google.com",
                "clients.google.com"
            ]

            # BLOCK LIST
            block_all = blocked_sites + [
               
                "tiktok.com",
                "reddit.com"
            ]

            for site in block_all:

                if site not in allow_list:

                    f.write(f"127.0.0.1 {site} #LAB_BLOCK\n")
                    f.write(f"127.0.0.1 www.{site} #LAB_BLOCK\n")

    except Exception as e:
        print("Host update error:", e)


# ===============================
# MAIN LOOP
# ===============================
while True:

    try:

        # ---------------------------
        # GET COMMAND
        # ---------------------------
        r = requests.get(
            COMMAND_API,
            params={"pc": PC_NAME},
            timeout=3
        )

        data = r.json()
        command = data.get("command", "none")

        print("📡 Command:", command)

        # ---------------------------
        # EXECUTE COMMAND
        # ---------------------------
        if command == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif command == "internet_off":
            os.system('netsh interface set interface "Wi-Fi" admin=disable')
            os.system('netsh interface set interface "Ethernet" admin=disable')

        elif command == "internet_on":
            os.system('netsh interface set interface "Wi-Fi" admin=enable')
            os.system('netsh interface set interface "Ethernet" admin=enable')

        elif command == "warning":
            show_warning("Admin warning!")

        # ---------------------------
        # GET SETTINGS
        # ---------------------------
        s = requests.get(SETTINGS_API, timeout=3).json()

        allowed_sites = s.get("allowed_sites", [])
        blocked_sites = s.get("blocked_sites", [])

        update_hosts(allowed_sites, blocked_sites)

    except Exception as e:
        print("⚠️ Agent error:", e)

    time.sleep(3)