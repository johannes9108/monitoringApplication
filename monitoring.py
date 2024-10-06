import logging, psutil, time, threading
from ui import UI 

class Monitoring:
    def __init__(self, logger, utils, fm):
        self.utils = utils
        self.fm = fm
        self.ui = UI(logger, self)
        self.logger = logger
        self.global_monitoring = False
        self.background_thread_running = False
        self.alarms = {"cpu_alarms":[],"memory_alarms":[],"disk_alarms":[]}
        self.fm.load_alarm_data()
    def start_monitoring(self):
        self.global_monitoring = True
        print("Monitoring started",end="\n\n")
    
    def check_alarms(self,usage_percent,alarm_type_values,alarm_type):
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
    def list_active_monitoring(self,halt=False):
        if self.global_monitoring == False:
            self.logger.info("No_monitoring_is_active")
            print("No monitoring is active",end="\n\n")
        else:
            cpu_usage_percent = psutil.cpu_percent()
            mem_usage_percent = psutil.virtual_memory().percent
            mem_usage = self.utils.convertBytesToGB(psutil.virtual_memory().used)
            mem_total = self.utils.convertBytesToGB(psutil.virtual_memory().total)
            disk_usage_percent = psutil.disk_usage('/').percent
            disk_usage = self.utils.convertBytesToGB(psutil.disk_usage('/').used)
            disk_total = self.utils.convertBytesToGB(psutil.disk_usage('/').total)
            if(self.background_thread_running):
                self.check_alarms(cpu_usage_percent,self.alarms["cpu_alarms"], "CPU")
                self.check_alarms(mem_usage_percent,self.alarms["memory_alarms"],"Memory")
                self.check_alarms(disk_usage_percent,self.alarms["disk_alarms"], "Disk")
            
            print(f"CPU Usage: {cpu_usage_percent}%", f"Memory Usage: {mem_usage_percent}% ({mem_usage} GB out of {mem_total} used)", f"Disk Usage: {disk_usage_percent}% ({disk_usage} GB out of {disk_total} used)", sep="\n",end="\n\n")
            self.logger.info("CPU_Usage_%d%%_Memory_Usage_%d%%_Disk_Usage_%d%%", cpu_usage_percent, mem_usage_percent, disk_usage_percent)
            self.ui.displayEndFrame(halt)
    def list_active_monitoring_wrapper(self):
        while self.background_thread_running:
            time.sleep(2)
            self.list_active_monitoring()
    def create_alarm(self):
        while True:
            self.ui.displayStartFrame("Create alarm")
            print("1 CPU Usage")
            print("2 Memory Usage")
            print("3 Disk Usage")
            print("4 Exit", end="\n\n")
            choice = int(input("Enter choice: "))
            if choice == 1:
                while True:
                    cpu_threshold = int(input("Enter CPU threshold between 1-100: "))
                    if not (self.utils.valid_threshold(cpu_threshold)):
                        continue
                    else:
                        self.alarms["cpu_alarms"].append(cpu_threshold)
                        print(f"Alarm for CPU usage set to {cpu_threshold}%")
                        break
            elif choice == 2:
                while True:
                    mem_threshold = int(input("Enter Memory threshold between 1-100: "))
                    if not (self.utils.valid_threshold(mem_threshold)):
                        continue
                    else: 
                        self.alarms["memory_alarms"].append(mem_threshold)
                        print(f"Alarm for Memory usage set to {mem_threshold}%")
                        break
            elif choice == 3:
                while True:
                    disk_threshold = int(input("Enter Disk threshold between 1-100: "))
                    if not (self.utils.valid_threshold(disk_threshold)):
                        continue
                    else:
                        self.alarms["disk_alarms"].append(disk_threshold)
                        print(f"Alarm for Disk usage set to {disk_threshold}%")
                        break
            elif choice == 4:
                print("Exit")
                break
            else:
                print("Invalid choice")
            self.ui.displayEndFrame()
        self.fm.persist_alarm_data()
    def remove_alarm(self):
        self.ui.displayStartFrame("Remove alarm")
        self.display_alarms(True)
        removable_candidate = int(input("Enter which alarm to remove: "))
        cpu_alarms = len(self.alarms.get("cpu_alarms"))
        memory_alarms = len(self.alarms.get("memory_alarms"))
        disk_alarms = len(self.alarms.get("disk_alarms"))
        if removable_candidate < 1 or removable_candidate > cpu_alarms + memory_alarms + disk_alarms:
            print("Invalid choice")
            return
        elif removable_candidate <= cpu_alarms:
            self.alarms["cpu_alarms"].remove(self.alarms["cpu_alarms"][removable_candidate-1])
        elif removable_candidate <= cpu_alarms + memory_alarms:
            self.alarms["memory_alarms"].remove(self.alarms["memory_alarms"][removable_candidate-cpu_alarms-1])
        elif removable_candidate <= cpu_alarms + memory_alarms + disk_alarms:
            self.alarms["disk_alarms"].remove(self.alarms["disk_alarms"][removable_candidate-cpu_alarms-memory_alarms-1])
        print(f"Alarm {removable_candidate} removed")
        self.fm.persist_alarm_data()
        time.sleep(1)
    def display_alarms(self,subMenu = False):
        self.alarms['cpu_alarms'].sort()
        self.alarms['memory_alarms'].sort()
        self.alarms['disk_alarms'].sort()
        totalAlarms = len(self.alarms.get("cpu_alarms")) + len(self.alarms.get("memory_alarms")) + len(self.alarms.get("disk_alarms"))
        count = 0
        print(totalAlarms)
        for i in range(len(self.alarms['cpu_alarms'])):
            count += 1
            print(f"{count}. CPU Alarm {self.alarms['cpu_alarms'][i]}%")
        for i in range(len(self.alarms['memory_alarms'])):
            count += 1
            print(f"{count}. Memory Alarm {self.alarms['memory_alarms'][i]}%")
        for i in range(len(self.alarms['disk_alarms'])):
            count += 1
            print(f"{count}. Disk Alarm {self.alarms['disk_alarms'][i]}%")
        if not subMenu:
            input("Press Enter to return to main menu...")
    def start_monitoring_mode(self):
        self.background_thread_running = True
        self.ui.displayStartFrame("Monitoring Mode Activated")
        continuous_monitoring_thread = threading.Thread(target=self.list_active_monitoring_wrapper, args=(), daemon=True)
        continuous_monitoring_thread.start()
        input("Press Enter to stop monitoring mode...\n")
        self.background_thread_running = False
        continuous_monitoring_thread.join()
