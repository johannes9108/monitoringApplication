# Monitoring Application for the course Systemutveckling i Python

# Read Menu options from a file
import os, psutil, time, math, threading, logging

logger = logging.getLogger(__name__)
global_monitoring = False
background_thread_running = False
menu_options = []
alarms = {
        "cpu_alarms": [1,2,3,4,10,20],
        "memory_alarms": [5,15,20,70,72],
        "disk_alarms": [20,30,35,40,60]
    }

## Utility Functions
def read_menu_options():
    logger.info("Reading_menu_options_from_file")
    global menu_options
    menu_options = []
    try:
        with open("menu_options.txt", "r",encoding='UTF-8') as file:
            for line in file:
                menu_options.append(line.strip())
    except FileNotFoundError:
        print("File not found")
def display_menu():
    displayStartFrame("Monitoring Application")
    for i in range(len(menu_options)):
        print(f"{i+1} {menu_options[i]}")
    print(f"{len(menu_options)+1} Exit\n")
    displayEndFrame()
def convertBytesToGB(bytes):
    return math.ceil(bytes/10**9)
def valid_threshold(threshold, min=1, max=100):
    if threshold < min or threshold > max:
        print("Invalid threshold", end="\n\n")
        return False
    return True
def displayStartFrame(title):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{title}\n{'-'*len(title)}",end="\n\n")
def displayEndFrame(halt=False):
    time.sleep(1)
    if halt == True:
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
def list_active_monitoring_wrapper():
    while background_thread_running:
        time.sleep(2)
        list_active_monitoring()
def check_alarms(usage_percent,alarm_type_values,alarm_type):
    minValue = 100
    alarm_triggered = False
    # absolute value of the difference between the current value and the alarm value
    for index, alarm in enumerate(alarm_type_values):
        if(usage_percent>=alarm):
            alarm_triggered = True
            if abs(usage_percent - alarm) <= minValue:
                minValue = abs(usage_percent - alarm)
                minValueIndex = index
                # print(f"CPU Usage alarm: {cpu_usage_percent}%")
    if alarm_triggered:
        print(f"Warning, Alarm triggered, {alarm_type} usage exceeds: {alarm_type_values[minValueIndex]}%")

## Initialization Functions
def init():
    logging.basicConfig(level=logging.INFO, filename="logs/monitoring.log", 
                        format="%(asctime)s_%(message)s", encoding="utf-8",
                        datefmt='%d/%m/%Y_%H:%M')
    logger.debug("Initializing Monitoring Application")
    logger.debug("Setting up logger")
    read_menu_options()
    time.sleep(1)


## Monitoring Functions
def start_monitoring():
    logger.info("Monitoring_started")
    global global_monitoring
    global_monitoring = True
    print(f"Monitoring started",end="\n\n")
    displayEndFrame()
def list_active_monitoring(halt=False):
    if global_monitoring == False:
        logger.info("No_monitoring_is_active")
        print("No monitoring is active",end="\n\n")
    else:
        cpu_usage_percent = psutil.cpu_percent()
        mem_usage_percent = psutil.virtual_memory().percent
        mem_usage = convertBytesToGB(psutil.virtual_memory().used)
        mem_total = convertBytesToGB(psutil.virtual_memory().total)
        disk_usage_percent = psutil.disk_usage('/').percent
        disk_usage = convertBytesToGB(psutil.disk_usage('/').used)
        disk_total = convertBytesToGB(psutil.disk_usage('/').total)
        if(background_thread_running):
            check_alarms(cpu_usage_percent,alarms["cpu_alarms"], "CPU")
            check_alarms(mem_usage_percent,alarms["memory_alarms"],"Memory")
            check_alarms(disk_usage_percent,alarms["disk_alarms"], "Disk")
        
        print(f"CPU Usage: {cpu_usage_percent}%", f"Memory Usage: {mem_usage_percent}% ({mem_usage} GB out of {mem_total} used)", f"Disk Usage: {disk_usage_percent}% ({disk_usage} GB out of {disk_total} used)", sep="\n",end="\n\n")
        logger.info("CPU_Usage_%d%%_Memory_Usage_%d%%_Disk_Usage_%d%%", cpu_usage_percent, mem_usage_percent, disk_usage_percent)
        displayEndFrame(halt)
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
def remove_alarm():
    displayStartFrame("Remove alarm")
    display_alarms(True)
    removable_candidate = int(input("Enter which alarm to remove: "))
    cpu_alarms = len(alarms.get("cpu_alarms"))
    memory_alarms = len(alarms.get("memory_alarms"))
    disk_alarms = len(alarms.get("disk_alarms"))
    if removable_candidate < 1 or removable_candidate > cpu_alarms + memory_alarms + disk_alarms:
        print("Invalid choice")
        return
    elif removable_candidate <= cpu_alarms:
        alarms["cpu_alarms"].remove(alarms["cpu_alarms"][removable_candidate-1])
    elif removable_candidate <= cpu_alarms + memory_alarms:
        alarms["memory_alarms"].remove(alarms["memory_alarms"][removable_candidate-cpu_alarms-1])
    elif removable_candidate <= cpu_alarms + memory_alarms + disk_alarms:
        alarms["disk_alarms"].remove(alarms["disk_alarms"][removable_candidate-cpu_alarms-memory_alarms-1])
    print(f"Alarm {removable_candidate} removed")
    time.sleep(1)
def display_alarms(subMenu = False):
    alarms['cpu_alarms'].sort()
    alarms['memory_alarms'].sort()
    alarms['disk_alarms'].sort()
    totalAlarms = len(alarms.get("cpu_alarms")) + len(alarms.get("memory_alarms")) + len(alarms.get("disk_alarms"))
    count = 0
    print(totalAlarms)
    for i in range(len(alarms['cpu_alarms'])):
        count += 1
        print(f"{count}. CPU Alarm {alarms['cpu_alarms'][i]}%")
    for i in range(len(alarms['memory_alarms'])):
        count += 1
        print(f"{count}. Memory Alarm {alarms['memory_alarms'][i]}%")
    for i in range(len(alarms['disk_alarms'])):
        count += 1
        print(f"{count}. Disk Alarm {alarms['disk_alarms'][i]}%")
    if not subMenu:
        input("Press Enter to return to main menu...")
def start_monitoring_mode():
    global background_thread_running
    background_thread_running = True
    displayStartFrame("Monitoring Mode Activated")
    continuous_monitoring_thread = threading.Thread(target=list_active_monitoring_wrapper, args=(), daemon=True)
    continuous_monitoring_thread.start()
    input("Press Enter to stop monitoring mode...\n")
    background_thread_running = False
    continuous_monitoring_thread.join()
        
def main():
    init()
    while True:
        display_menu()
        try: 
            choice = int(input("Enter choice: "))
            if choice == 1:
                start_monitoring()
            elif choice == 2:
                list_active_monitoring(True)
            elif choice == 3:
                create_alarm()
            elif choice == 4:
                remove_alarm()
            elif choice == 5:
                display_alarms()
            elif choice == 6:
                start_monitoring_mode()
            elif choice == len(menu_options)+1:
                print("Exit")
                break
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")
            continue
main()