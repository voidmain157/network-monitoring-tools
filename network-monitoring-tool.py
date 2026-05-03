from netmiko import ConnectHandler
import time
from datetime import datetime

router = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'admin'
}

targets = [
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.3",
    "192.168.1.4"
]

def log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

def monitor():
    while True:
        try:
            log("Connecting to router...")
            conn = ConnectHandler(**router)

            log("Checking interface...")
            interfaces = conn.send_command("show ip interface brief")
            print(interfaces)

            log("Running ping test...")

            for ip in targets:
                result = conn.send_command(f"ping {ip}")

                if "Success rate is 100 percent" in result:
                    log(f"[OK] {ip} UP")
                elif "Success rate is 80 percent" in result:
                    log(f"[WARNING] {ip} UNSTABLE")
                else:
                    log(f"[ALERT] {ip} DOWN !!!")

            conn.disconnect()

        except Exception as e:
            log(f"[ERROR] Tidak bisa connect ke router: {e}")

        log("Menunggu 10 detik...\n")
        time.sleep(10)


if __name__ == "__main__":
    monitor()
