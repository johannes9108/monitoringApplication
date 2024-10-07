"""Module will handle reading and writing to files"""

import json


class FileManager:
    """Class that handles reading and writing to files"""

    def __init__(self, logger, utils):
        # Fix the constructors to take in logger as a parameter
        self.logger = logger
        self.utils = utils
        self.logger.info("Initializing FileManager")

    def readMenuOptions(self):
        """
        Reading menu options from txt-file
        """
        self.logger.debug("Reading_menu_options_from_file")
        menuOptions = []
        try:
            with open("data/menuOptions.txt", "r", encoding="UTF-8") as file:
                for line in file:
                    menuOptions.append(line.strip())
                return menuOptions
        except FileNotFoundError:
            print("File not found")

    def persistAlarmData(self, alarms):
        """
        Using basic IO to write alarms to a json file
        """
        try:
            with open("data/alarms.json", "w", encoding="UTF-8") as file:
                file.write(json.dumps(alarms))
                self.utils.output("Alarms saved to alarms.json", True, True)
        except FileNotFoundError:
            print("File not found")

    def loadAlarmData(self):
        """
        Using basic IO to read alarms from a json file
        """
        try:
            with open("data/alarms.json", "r", encoding="UTF-8") as file:
                alarms = json.load(file)
                self.utils.output("loading previously configured alarms...", True, True)
                return alarms
        except FileNotFoundError:
            print("File not found")
