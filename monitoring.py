"""
    Core Module for the Monitoring Application
    """

from operator import le
from re import U, sub
import time, threading, logging
import psutil
from prometheus_client import Gauge
import ui
from Alarm import Alarm
# Define a Prometheus Counter metric
# CLI_COMMAND_COUNTER = Counter('cli_command_runs_total', 'Total number of CLI commands executed')
CPU_Usage_Percent = Gauge("cpu_usage_percent", "Current CPU Usage in Percent")
Memory_Usage_Percent = Gauge("memory_usage_percent", "Current Memory Usage in Percent")
Disk_Usage_Percent = Gauge("disk_usage_percent", "Current Disk Usage in Percent")
JSON_FILENAME = "alarmData.json"

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
        self.alarms = fm.loadAlarmData(JSON_FILENAME)
        self.logger = logger
        self.logger.info("Initializing Monitoring Application")

    def startMonitoring(self):
        """
        Activates the ability to monitor the system
        """
        self.globalMonitoring = True
        self.utils.output("Monitoring started", console=True, logger=True, level=logging.INFO)
        ui.UI.displayEndFrame()

    def checkAlarms(self, usagePercent, alarmTypeValues, alarmType):
        """
        Checks if the current usage exceeds the alarm value
        """
        minValue = 100655
        alarmTriggered = False
        # absolute value of the difference between the current value and the alarm value
        for index, alarm in enumerate(alarmTypeValues):
            if usagePercent >= alarm.level:
                alarmTriggered = True
                if abs(usagePercent - alarm.level) <= minValue:
                    minValue = abs(usagePercent - alarm.level)
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
            self.utils.output( f"CPU Usage: {cpuUsagePercent}%",
                f"Memory Usage: {memUsagePercent}% ({memUsage} GB out of {memTotal} used)",
                f"Disk Usage: {diskUsagePercent}% ({diskUsage} GB out of {diskTotal} used)",
                console=True, logger=True, level=logging.DEBUG)
            if self.backgroundThreadRunning:
                self.checkAlarms(cpuUsagePercent, list(filter(lambda x: x.type == "CPU",self.alarms)), "CPU")
                self.checkAlarms(memUsagePercent, list(filter(lambda x: x.type == "Memory",self.alarms)), "Memory")
                self.checkAlarms(diskUsagePercent, list(filter(lambda x: x.type == "Disk",self.alarms)), "Disk")
                CPU_Usage_Percent.set(cpuUsagePercent)
                Memory_Usage_Percent.set(memUsagePercent)
                Disk_Usage_Percent.set(diskUsagePercent)
                self.utils.output(self.utils.LINEBREAK, console=True, logger=False)

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
            if choice == 4:
                self.utils.output("Exit",console=True, logger=False)
                break
            self.addNewAlarms(choice, self.alarms)
            ui.UI.displayEndFrame()
        self.fm.persistAlarmData(self.alarms,JSON_FILENAME)
    def addNewAlarms(self,choice, alarms):
        if choice in range(1,4):
            choice = ["CPU","Memory","Disk"].__getitem__(choice-1)
            while True:
                thresHold = int(ui.UI.input(f"Enter {choice} threshold between 1-100: "))
                if not self.utils.validThreshold(thresHold):
                    continue
                else:
                    alarms.append(Alarm(thresHold, choice))
                    self.utils.output(f"Alarm for {choice} usage set to {thresHold}%",console=True, logger=True, level=logging.INFO)
                    break
        else:
            self.utils.output("Invalid choice",console=True, logger=False)
    def removeAlarm(self):
        """
        Removes a selected alarm from the alarms dictionary
        """
        ui.UI.displayStartFrame("Remove alarm")
        self.displayAlarms(True)
        removableCandidate = int(ui.UI.input("Enter which alarm to remove: "))
        try:
            if removableCandidate in range(1,len(self.alarms)+1):
                self.alarms.pop(removableCandidate-1)
            else :
                raise IndexError
        except IndexError:
            self.utils.output("Invalid alarm index",console=True, logger=True, level=logging.ERROR)
            return
        self.utils.output(f"Alarm {removableCandidate} removed",console=True, logger=True, level=logging.INFO)
        self.fm.persistAlarmData(self.alarms,JSON_FILENAME)
        time.sleep(1)

    def displayAlarms(self, subMenu=False):
        """
        Displays the alarms in the alarms dictionary, sorts them by type and level
        """
        self.logger.debug("Displaying_alarms")
        if len(self.alarms) == 0:
            self.utils.output("No alarms set",console=True, logger=True, level=logging.INFO)
        else:
            self.alarms = sorted(self.alarms, key=lambda alarm: (alarm.type, alarm.level))
            ui.UI.displayAlarms(self.alarms,subMenu)
        ui.UI.displayEndFrame()

    def startMonitoringMode(self):
        """
        Activates monitoring mode
        """
        if self.globalMonitoring == False:
            self.utils.output("No monitoring is active", console=True, logger=True, level=logging.INFO)
        else:
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
        ui.UI.displayEndFrame()
    def run(self):
        """
        Main function to run the monitoring application
        """

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
                elif choice == len(ui.UI.menuOptions) + 1:
                    break
                else:
                    self.utils.output(f"Invalid choice - Integer ${choice} is not a viable option",
                                      console=True, logger=False, level=logging.ERROR)
                    ui.UI.displayEndFrame()
            except ValueError:
                self.utils.output("Invalid choice - Not an integer", console=True, logger=False, level=logging.ERROR)
                ui.UI.displayEndFrame()

