"""
    Core Module for the Monitoring Application
    """

import time, threading, logging
import psutil
from prometheus_client import Gauge
import ui


# Define a Prometheus Counter metric
# CLI_COMMAND_COUNTER = Counter('cli_command_runs_total', 'Total number of CLI commands executed')
CPU_Usage_Percent = Gauge("cpu_usage_percent", "Current CPU Usage in Percent")
Memory_Usage_Percent = Gauge("memory_usage_percent", "Current Memory Usage in Percent")
Disk_Usage_Percent = Gauge("disk_usage_percent", "Current Disk Usage in Percent")


class Monitoring:
    """
    Monitoring Application for the course Systemutveckling i Python
    Contains the business logic for the monitoring application and CLI functionality
    """

    def __init__(self, logger, utils, fm):
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
        self.utils.output("Monitoring_started", console=True, logger=True, level=logging.INFO)
        ui.UI.displayEndFrame()

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
        if alarmTriggered:
            self.utils.output(f"Warning, Alarm triggered, {alarmType} usage exceeds: {alarmTypeValues[minValueIndex]}%",
                              console=True, logger=True,level=logging.WARNING)

    def listActiveMonitoring(self, halt=False):
        """
        Displays the current system usage
        """
        if self.globalMonitoring == False:
            self.utils.output("No monitoring is active", console=True, logger=True, level=logging.INFO)
        else:
            cpuUsagePercent = psutil.cpu_percent()
            memUsagePercent = psutil.virtual_memory().percent
            memUsage = self.utils.convertBytesToGB(psutil.virtual_memory().used)
            memTotal = self.utils.convertBytesToGB(psutil.virtual_memory().total)
            diskUsagePercent = psutil.disk_usage("/").percent
            diskUsage = self.utils.convertBytesToGB(psutil.disk_usage("/").used)
            diskTotal = self.utils.convertBytesToGB(psutil.disk_usage("/").total)
            if self.backgroundThreadRunning:
                self.checkAlarms(cpuUsagePercent, self.alarms["cpuAlarms"], "CPU")
                self.checkAlarms(memUsagePercent, self.alarms["memoryAlarms"], "Memory")
                self.checkAlarms(diskUsagePercent, self.alarms["diskAlarms"], "Disk")
                CPU_Usage_Percent.set(cpuUsagePercent)
                Memory_Usage_Percent.set(memUsagePercent)
                Disk_Usage_Percent.set(diskUsagePercent)
            self.utils.output( f"CPU Usage: {cpuUsagePercent}%",
                f"Memory Usage: {memUsagePercent}% ({memUsage} GB out of {memTotal} used)",
                f"Disk Usage: {diskUsagePercent}% ({diskUsage} GB out of {diskTotal} used)",
                console=True, logger=True, level=logging.DEBUG)

        ui.UI.displayEndFrame(halt)

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
            ui.UI.displayStartFrame("Create alarm")
            ui.UI.displayMenu(["CPU Usage", "Memory Usage", "Disk Usage", "Exit"])
            choice = int(ui.UI.input("Enter choice: "))
            if choice == 1:
                while True:
                    cpuThreshold = int(ui.UI.input("Enter CPU threshold between 1-100: "))
                    if not self.utils.validThreshold(cpuThreshold):
                        continue
                    else:
                        self.alarms["cpuAlarms"].append(cpuThreshold)
                        self.utils.output(f"Alarm for CPU usage set to {cpuThreshold}%",console=True, logger=True, level=logging.INFO)
                        break
            elif choice == 2:
                while True:
                    memThreshold = int(ui.UI.input("Enter Memory threshold between 1-100: "))
                    if not self.utils.validThreshold(memThreshold):
                        continue
                    else:
                        self.alarms["memoryAlarms"].append(memThreshold)
                        self.utils.output(f"Alarm for Memory usage set to {memThreshold}%",console=True, logger=True, level=logging.INFO)

                        break
            elif choice == 3:
                while True:
                    diskThreshold = int(ui.UI.input("Enter Disk threshold between 1-100: "))
                    if not self.utils.validThreshold(diskThreshold):
                        continue
                    else:
                        self.alarms["diskAlarms"].append(diskThreshold)
                        self.utils.output(f"Alarm for Disk usage set to {diskThreshold}%",console=True, logger=True, level=logging.INFO)
                        break
            elif choice == 4:
                self.utils.output("Exit",console=True, logger=False)
                break
            else:
                self.utils.output("Invalid choice",console=True, logger=False)
            ui.UI.displayEndFrame()
        self.fm.persistAlarmData(self.alarms)

    def removeAlarm(self):
        """
        Removes a selected alarm from the alarms dictionary
        """
        ui.UI.displayStartFrame("Remove alarm")
        self.displayAlarms(True)
        removableCandidate = int(ui.UI.input("Enter which alarm to remove: "))
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
        self.utils.output(f"Alarm {removableCandidate} removed",console=True, logger=True, level=logging.INFO)
        self.fm.persistAlarmData(self.alarms)
        time.sleep(1)

    def displayAlarms(self, subMenu=False):
        """
        Displays the alarms in the alarms dictionary
        """
        self.alarms["cpuAlarms"].sort()
        self.alarms["memoryAlarms"].sort()
        self.alarms["diskAlarms"].sort()
        self.logger.debug("Displaying_alarms")
        ui.UI.displayAlarms(self.alarms,subMenu)

    def startMonitoringMode(self):
        """
        Activates monitoring mode
        """
        self.backgroundThreadRunning = True
        ui.UI.displayStartFrame("Monitoring Mode Activated")
        self.utils.output("Monitoring Mode Activated", console=False, logger=True, level=logging.INFO)
        continuousMonitoringThread = threading.Thread(
            target=self.listActiveMonitoringWrapper, args=(), daemon=True
        )
        continuousMonitoringThread.start()
        ui.UI.input("Press Enter to stop monitoring mode...\n")
        self.backgroundThreadRunning = False
        continuousMonitoringThread.join()

    def run(self):
        """
        Main function to run the monitoring application
        """
        self.menuOptions = self.fm.readMenuOptions()
        while True:
            ui.UI.displayMenu()
            try:
                choice = int(ui.UI.input("Enter choice: "))
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
                    self.utils.output(f"Invalid choice - Integer ${choice} is not a viable option",
                                      console=True, logger=False, level=logging.ERROR)
                    ui.UI.displayEndFrame()
            except ValueError:
                self.utils.output("Invalid choice - Not an integer", console=True, logger=False, level=logging.ERROR)
                ui.UI.displayEndFrame()

