import psutil
import pandas as pd
import time
from datetime import datetime

CPU_THRESHOLD = 80
MEM_THRESHOLD = 80
DISK_THRESHOLD = 90

LOG_FILE = "system_logs.csv"

def log_system_stats():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

    data = {"time": timestamp, "cpu": cpu, "memory": memory, "disk": disk, "network_bytes": net}
    df = pd.DataFrame([data])
    df.to_csv(LOG_FILE, mode='a', header=not pd.io.common.file_exists(LOG_FILE), index=False)

    if cpu > CPU_THRESHOLD:
        print(f"⚠️ High CPU usage: {cpu}%")
    if memory > MEM_THRESHOLD:
        print(f"⚠️ High Memory usage: {memory}%")
    if disk > DISK_THRESHOLD:
        print(f"⚠️ Disk almost full: {disk}%")

def main():
    print("🔍 Starting system monitor (press Ctrl+C to stop)...")
    try:
        while True:
            log_system_stats()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")

if __name__ == "__main__":
    main()
