"""
    Core Module for the Monitoring Application
    """

import os, time, threading
import psutil


class Monitoring:
    """
    Monitoring Application for the course Systemutveckling i Python
    Contains the business logic for the monitoring application and CLI functionality
    """

    def __init__(self, logger, utils, fm, cliCounter):
        self.cliCounter = cliCounter
        self.utils = utils
        self.fm = fm
        self.logger = logger
        self.globalMonitoring = False
        self.backgroundThreadRunning = False
        self.menuOptions = fm.readMenuOptions()
        self.alarms = fm.loadAlarmData()
        self.logger = logger
        self.logger.info("Initializing Monitoring Application")

    def startMonitoring(self):
        """
        Activates the ability to monitor the system
        """
        self.globalMonitoring = True
        self.utils.output("Monitoring_started", True, True, "\n\n")
        self.displayEndFrame()

    def checkAlarms(self, usagePercent, alarmTypeValues, alarmType):
        """
        Checks if the current usage exceeds the alarm value
        """
        minValue = 100
        alarmTriggered = False
        # absolute value of the difference between the current value and the alarm value
        for index, alarm in enumerate(alarmTypeValues):
            if usagePercent >= alarm:
                alarmTriggered = True
                if abs(usagePercent - alarm) <= minValue:
                    minValue = abs(usagePercent - alarm)
                    minValueIndex = index
                    # print(f"CPU Usage alarm: {cpuUsagePercent}%")
        if alarmTriggered:
            print(
                f"Warning, Alarm triggered, {alarmType} usage exceeds: {alarmTypeValues[minValueIndex]}%"
            )
            self.logger.warning(
                "Warning_Alarm_triggered_%s_usage_exceeds_%d%%",
                alarmType,
                alarmTypeValues[minValueIndex],
            )

    def listActiveMonitoring(self, halt=False):
        """
        Displays the current system usage
        """
        if self.globalMonitoring == False:
            self.logger.info("No_monitoring_is_active")
            self.logger.warning("No_monitoring_is_active")
            print("No monitoring is active", end="\n\n")
        else:
            cpuUsagePercent = psutil.cpu_percent()
            memUsagePercent = psutil.virtual_memory().percent
            memUsage = self.utils.convertBytesToGB(psutil.virtual_memory().used)
            memTotal = self.utils.convertBytesToGB(psutil.virtual_memory().total)
            diskUsagePercent = psutil.disk_usage("/").percent
            diskUsage = self.utils.convertBytesToGB(psutil.disk_usage("/").used)
            diskTotal = self.utils.convertBytesToGB(psutil.disk_usage("/").total)
            if self.backgroundThreadRunning:
                self.checkAlarms(cpuUsagePercent, self.alarms["cpu_alarms"], "CPU")
                self.checkAlarms(memUsagePercent, self.alarms["memoryAlarms"], "Memory")
                self.checkAlarms(diskUsagePercent, self.alarms["diskAlarms"], "Disk")

            print(
                f"CPU Usage: {cpuUsagePercent}%",
                f"Memory Usage: {memUsagePercent}% ({memUsage} GB out of {memTotal} used)",
                f"Disk Usage: {diskUsagePercent}% ({diskUsage} GB out of {diskTotal} used)",
                sep="\n",
                end="\n\n",
            )
            self.logger.debug(
                "CPU_Usage_%d%%_Memory_Usage_%d%%_Disk_Usage_%d%%",
                cpuUsagePercent,
                memUsagePercent,
                diskUsagePercent,
            )
        self.displayEndFrame(halt)

    def listActiveMonitoringWrapper(self):
        """
        Helper function to run listActiveMonitoring in a separate thread
        """
        while self.backgroundThreadRunning:
            time.sleep(2)
            self.listActiveMonitoring()

    def createAlarm(self):
        """
        Adds an alarm to the alarms dictionary
        """
        while True:
            self.displayStartFrame("Create alarm")
            print("1 CPU Usage")
            print("2 Memory Usage")
            print("3 Disk Usage")
            print("4 Exit", end="\n\n")
            choice = int(input("Enter choice: "))
            if choice == 1:
                while True:
                    cpuThreshold = int(input("Enter CPU threshold between 1-100: "))
                    if not self.utils.validThreshold(cpuThreshold):
                        continue
                    else:
                        self.alarms["cpuAlarms"].append(cpuThreshold)
                        print(f"Alarm for CPU usage set to {cpuThreshold}%")
                        self.logger.info(
                            "Alarm_for_CPU_usage_set_to_%d%%", cpuThreshold
                        )
                        break
            elif choice == 2:
                while True:
                    memThreshold = int(input("Enter Memory threshold between 1-100: "))
                    if not self.utils.validThreshold(memThreshold):
                        continue
                    else:
                        self.alarms["memoryAlarms"].append(memThreshold)
                        print(f"Alarm for Memory usage set to {memThreshold}%")
                        self.logger.info(
                            "Alarm_for_Memory_usage_set_to_%d%%", memThreshold
                        )
                        break
            elif choice == 3:
                while True:
                    diskThreshold = int(input("Enter Disk threshold between 1-100: "))
                    if not self.utils.validThreshold(diskThreshold):
                        continue
                    else:
                        self.alarms["diskAlarms"].append(diskThreshold)
                        print(f"Alarm for Disk usage set to {diskThreshold}%")
                        self.logger.info(
                            "Alarm_for_Disk_usage_set_to_%d%%", diskThreshold
                        )
                        break
            elif choice == 4:
                print("Exit")
                break
            else:
                print("Invalid choice")
            self.displayEndFrame()
        self.fm.persistAlarmData(self.alarms)

    def removeAlarm(self):
        """
        Removes a selected alarm from the alarms dictionary
        """
        self.displayStartFrame("Remove alarm")
        self.displayAlarms(True)
        removableCandidate = int(input("Enter which alarm to remove: "))
        cpuAlarms = len(self.alarms.get("cpuAlarms"))
        memoryAlarms = len(self.alarms.get("memoryAlarms"))
        diskAlarms = len(self.alarms.get("diskAlarms"))
        if (
            removableCandidate < 1
            or removableCandidate > cpuAlarms + memoryAlarms + diskAlarms
        ):
            print("Invalid choice")
            return
        elif removableCandidate <= cpuAlarms:
            self.alarms["cpuAlarms"].remove(
                self.alarms["cpuAlarms"][removableCandidate - 1]
            )
        elif removableCandidate <= cpuAlarms + memoryAlarms:
            self.alarms["memoryAlarms"].remove(
                self.alarms["memoryAlarms"][removableCandidate - cpuAlarms - 1]
            )
        elif removableCandidate <= cpuAlarms + memoryAlarms + diskAlarms:
            self.alarms["diskAlarms"].remove(
                self.alarms["diskAlarms"][
                    removableCandidate - cpuAlarms - memoryAlarms - 1
                ]
            )
        print(f"Alarm {removableCandidate} removed")
        self.logger.info("Alarm_%d_removed", removableCandidate)
        self.fm.persistAlarmData(self.alarms)
        time.sleep(1)

    def displayAlarms(self, subMenu=False):
        """
        Displays the alarms in the alarms dictionary
        """
        self.alarms["cpuAlarms"].sort()
        self.alarms["memoryAlarms"].sort()
        self.alarms["diskAlarms"].sort()
        count = 0
        self.logger.debug("Displaying_alarms")
        for i in range(len(self.alarms["cpuAlarms"])):
            count += 1
            print(f"{count}. CPU Alarm {self.alarms['cpuAlarms'][i]}%")
        for i in range(len(self.alarms["memoryAlarms"])):
            count += 1
            print(f"{count}. Memory Alarm {self.alarms['memoryAlarms'][i]}%")
        for i in range(len(self.alarms["diskAlarms"])):
            count += 1
            print(f"{count}. Disk Alarm {self.alarms['diskAlarms'][i]}%")
        if not subMenu:
            input("Press Enter to return to main menu...")

    def startMonitoringMode(self):
        """
        Activates monitoring mode
        """
        self.backgroundThreadRunning = True
        self.displayStartFrame("Monitoring Mode Activated")
        self.logger.info("Monitoring_Mode_Activated")
        continuousMonitoringThread = threading.Thread(
            target=self.listActiveMonitoringWrapper, args=(), daemon=True
        )
        continuousMonitoringThread.start()
        input("Press Enter to stop monitoring mode...\n")
        self.backgroundThreadRunning = False
        continuousMonitoringThread.join()

    def run(self):
        """
        Main function to run the monitoring application
        """
        self.menuOptions = self.fm.readMenuOptions()
        while True:
            self.displayMenu()
            try:
                choice = int(input("Enter choice: "))
                self.cliCounter.inc()
                if choice == 1:
                    self.startMonitoring()
                elif choice == 2:
                    self.listActiveMonitoring(True)
                elif choice == 3:
                    self.createAlarm()
                elif choice == 4:
                    self.removeAlarm()
                elif choice == 5:
                    self.displayAlarms()
                elif choice == 6:
                    self.startMonitoringMode()
                elif choice == len(self.menuOptions) + 1:
                    break
                else:
                    print("Invalid choice")
                    self.displayEndFrame()
            except ValueError:
                print("Invalid choice")
                self.displayEndFrame()

    def displayMenu(self):
        """
        Displays the main menu
        """
        self.displayStartFrame("Monitoring Application")
        for index, option in enumerate(self.menuOptions):
            print(f"{index+1} {option}")
        print(f"{len(self.menuOptions)+1} Exit\n")
        self.displayEndFrame()

    def displayStartFrame(self, title):
        """
        Displays the start frame with a title of the CLI
        """
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{title}\n{'-'*len(title)}", end="\n\n")

    def displayEndFrame(self, halt=False):
        """
        Displays the end frame with a prompt to continue depending on the halt parameter
        """
        time.sleep(1)
        if halt == True:
            input("Press Enter to continue...")
            os.system("cls" if os.name == "nt" else "clear")
