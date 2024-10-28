"""Module will handle reading and writing to files"""

import json
from re import A
from utility import Utility as utils
from Alarm import Alarm

class FileManager:
    """Class that handles reading and writing to files"""

    def __init__(self):
        # Fix the constructors to take in logger as a parameter
        utils.output("Initializing FileManager", console=True, logger=True)
    def persistAlarmData(self, alarms,filename):
        """
        Using basic IO to write alarms to a json file
        """
        try:
            with open(f"data/{filename}", "w", encoding="UTF-8") as file:
                file.write(json.dumps(alarms,default=lambda o: o.serialize(),indent=4))
                utils.output("Alarms saved to alarms.json", console=True, logger=True)
        except FileNotFoundError:
            utils.output("File not found", console=True, logger=True, level=40)
        input("Press Enter to continue...")
    def loadAlarmData(self,filename):
        """
        Using basic IO to read alarms from a json file
        """
        try:
            with open(f"data/{filename}", "r", encoding="UTF-8") as file:
                alarms_dict = json.load(file)
                alarms = [Alarm.deserializer(alarm) for alarm in alarms_dict]
                utils.output("loading previously configured alarms...", console=True, logger=True)
                return alarms
        except FileNotFoundError:
            utils.output("File not found", console=True, logger=True, level=40)
            return []
