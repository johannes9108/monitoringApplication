import logging, psutil, time, threading,os

class Monitoring:
    def __init__(self, logger, utils, fm):
        self.utils = utils
        self.fm = fm
        self.logger = logger
        self.global_monitoring = False
        self.background_thread_running = False
        self.menu_options = fm.read_menu_options()
        self.alarms = fm.load_alarm_data()
        self.logger = logger
        logger.info("Initializing Monitoring Application")
        
    def start_monitoring(self):
        self.global_monitoring = True
        print("Monitoring started",end="\n\n")
        self.displayEndFrame()
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
            self.logger.debug("CPU_Usage_%d%%_Memory_Usage_%d%%_Disk_Usage_%d%%", cpu_usage_percent, mem_usage_percent, disk_usage_percent)
            self.displayEndFrame(halt)
    def list_active_monitoring_wrapper(self):
        while self.background_thread_running:
            time.sleep(2)
            self.list_active_monitoring()
    def create_alarm(self):
        while True:
            self.displayStartFrame("Create alarm")
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
            self.displayEndFrame()
        self.fm.persist_alarm_data()
    def remove_alarm(self):
        self.displayStartFrame("Remove alarm")
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
        self.displayStartFrame("Monitoring Mode Activated")
        continuous_monitoring_thread = threading.Thread(target=self.list_active_monitoring_wrapper, args=(), daemon=True)
        continuous_monitoring_thread.start()
        input("Press Enter to stop monitoring mode...\n")
        self.background_thread_running = False
        continuous_monitoring_thread.join()
        
    def run(self):
        self.menu_options = self.fm.read_menu_options()
        while True:
            self.display_menu()
            try: 
                choice = int(input("Enter choice: "))
                if choice == 1:
                    self.start_monitoring()
                elif choice == 2:
                    self.list_active_monitoring(True)
                elif choice == 3:
                    self.create_alarm()
                elif choice == 4:
                    self.remove_alarm()
                elif choice == 5:
                    self.display_alarms()
                elif choice == 6:
                    self.start_monitoring_mode()
                elif choice == len(self.menu_options)+1:
                    break
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")
    def display_menu(self):
        self.displayStartFrame("Monitoring Application")
        for i in range(len(self.menu_options)):
            print(f"{i+1} {self.menu_options[i]}")
        print(f"{len(self.menu_options)+1} Exit\n")
        self.displayEndFrame()
    def displayStartFrame(self,title):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{title}\n{'-'*len(title)}",end="\n\n")
    def displayEndFrame(self,halt=False):
        time.sleep(1)
        if halt == True:
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
