# Monitoring Application for the course Systemutveckling i Python

# Read Menu options from a file
import os, psutil

global_monitoring = False
menu_options = []

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
    menu_options = read_menu_options()
    for i in range(len(menu_options)):
        print(f"{i+1} {menu_options[i]}")
    print(f"{len(menu_options)+1} Exit\n")
def convertBytesToGB(bytes):
    import math
    return math.ceil(bytes/10**9)


## Monitoring Functions
def start_monitoring():
    global global_monitoring
    global_monitoring = True
    print(f"Monitoring started",end="\n\n")
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
        input("Press Enter to continue...")
def create_alarm():
    print("Create alarm")
def display_alarms():
    print("Display alarms")
def start_monitoring_mode():
    print("Start monitoring mode")
while True:
    display_menu()
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