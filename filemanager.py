"""Module will handle reading and writing to files"""

import json
from utility import Utility as utils


class FileManager:
    """Class that handles reading and writing to files"""

    def __init__(self):
        # Fix the constructors to take in logger as a parameter
        utils.output("Initializing FileManager", console=True, logger=True)
    def persistAlarmData(self, alarms):
        """
        Using basic IO to write alarms to a json file
        """
        try:
            with open("data/alarms.json", "w", encoding="UTF-8") as file:
                file.write(json.dumps(alarms))
                utils.output("Alarms saved to alarms.json", console=True, logger=True)
        except FileNotFoundError:
            utils.output("File not found", console=True, logger=True, level=40)

    def loadAlarmData(self):
        """
        Using basic IO to read alarms from a json file
        """
        try:
            with open("data/alarms.json", "r", encoding="UTF-8") as file:
                alarms = json.load(file)
                utils.output("loading previously configured alarms...", console=True, logger=True)
                return alarms
        except FileNotFoundError:
            utils.output("File not found", console=True, logger=True, level=40)
