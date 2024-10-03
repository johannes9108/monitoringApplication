# Monitoring Application for the course Systemutveckling i Python

# Read Menu options from a file
import os, psutil

global_monitoring = False
menu_options = []
alarms = {
        "cpu_alarms": [],
        "memory_alarms": [],
        "disk_alarms": []
    }

## Utility Functions
def read_menu_options():
    global menu_options
    menu_options = []
    try:
        with open("menu_options.txt", "r",encoding='UTF-8') as file:
            for line in file:
                menu_options.append(line.strip())
    except FileNotFoundError:
        print("File not found")
    return menu_options
def display_menu():
    displayStartFrame("Monitoring Application")
    menu_options = read_menu_options()
    for i in range(len(menu_options)):
        print(f"{i+1} {menu_options[i]}")
    print(f"{len(menu_options)+1} Exit\n")
def convertBytesToGB(bytes):
    import math
    return math.ceil(bytes/10**9)
def valid_threshold(threshold, min=1, max=100):
    if threshold < min or threshold > max:
        print("Invalid threshold", end="\n\n")
        return False
    return True
def displayStartFrame(title):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{title}\n{'-'*len(title)}",end="\n\n")
def displayEndFrame():
    import time
    time.sleep(1)
    input("Press Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')


## Monitoring Functions
def start_monitoring():
    global global_monitoring
    global_monitoring = True
    print(f"Monitoring started",end="\n\n")
    displayEndFrame()
def list_active_monitoring():
    if global_monitoring == False:
        print("No monitoring is active",end="\n\n")
    else:
        cpu_usage_percent = psutil.cpu_percent()
        mem_usage_percent = psutil.virtual_memory().percent
        mem_usage = convertBytesToGB(psutil.virtual_memory().used)
        mem_total = convertBytesToGB(psutil.virtual_memory().total)
        disk_usage_percent = psutil.disk_usage('/').percent
        disk_usage = convertBytesToGB(psutil.disk_usage('/').used)
        disk_total = convertBytesToGB(psutil.disk_usage('/').total)
        print(f"CPU Usage: {cpu_usage_percent}%", f"Memory Usage: {mem_usage_percent}% ({mem_usage} GB out of {mem_total} used)", f"Disk Usage: {disk_usage_percent}% ({disk_usage} GB out of {disk_total} used)", sep="\n",end="\n\n")
        displayEndFrame()
def create_alarm():
    while True:
        displayStartFrame("Create alarm")
        print("1 CPU Usage")
        print("2 Memory Usage")
        print("3 Disk Usage")
        print("4 Exit", end="\n\n")
        choice = int(input("Enter choice: "))
        if choice == 1:
            while True:
                cpu_threshold = int(input("Enter CPU threshold between 1-100: "))
                if not (valid_threshold(cpu_threshold)):
                    continue
                else:
                    alarms["cpu_alarms"].append(cpu_threshold)
                    print(f"Alarm for CPU usage set to {cpu_threshold}%")
                    break
        elif choice == 2:
            while True:
                mem_threshold = int(input("Enter Memory threshold between 1-100: "))
                if not (valid_threshold(mem_threshold)):
                    continue
                else: 
                    alarms["memory_alarms"].append(mem_threshold)
                    print(f"Alarm for Memory usage set to {mem_threshold}%")
                    break
        elif choice == 3:
            while True:
                disk_threshold = int(input("Enter Disk threshold between 1-100: "))
                if not (valid_threshold(disk_threshold)):
                    continue
                else:
                    alarms["disk_alarms"].append(disk_threshold)
                    print(f"Alarm for Disk usage set to {disk_threshold}%")
                    break
        elif choice == 4:
            print("Exit")
            break
        else:
            print("Invalid choice")
        displayEndFrame()
def display_alarms():
    alarms['cpu_alarms'].sort()
    alarms['memory_alarms'].sort()
    alarms['disk_alarms'].sort()
    totalAlarms = len(alarms.get("cpu_alarms")) + len(alarms.get("memory_alarms")) + len(alarms.get("disk_alarms"))
    count = 0
    print(totalAlarms)
    for i in range(len(alarms['cpu_alarms'])):
        count += 1
        print(f"CPU Alarm {count}: {alarms['cpu_alarms'][i]}%")
    for i in range(len(alarms['memory_alarms'])):
        count += i
        print(f"Memory Alarm {i+1}: {alarms['memory_alarms'][i]}%")
    for i in range(len(alarms['disk_alarms'])):
        count += i
        print(f"Disk Alarm {i+1}: {alarms['disk_alarms'][i]}%")    
    displayEndFrame()
def start_monitoring_mode():
    print("Start monitoring mode")
while True:
    display_menu()
    try: 
        choice = int(input("Enter choice: "))
        if choice == 1:
            start_monitoring()
        elif choice == 2:
            list_active_monitoring()
        elif choice == 3:
            create_alarm()
        elif choice == 4:
            display_alarms()
        elif choice == 5:
            start_monitoring_mode()
        elif choice == len(menu_options)+1:
            print("Exit")
            break
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid choice")
        continue