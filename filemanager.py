import json

class FileManager:
    def __init__(self, logger):
        # Fix the constructors to take in logger as a parameter
        self.logger = logger
        logger.info("Initializing FileManager")
    def read_menu_options(self):
        # self.logger.info("Reading_menu_options_from_file")
        menu_options = []
        try:
            with open("data/menu_options.txt", "r",encoding='UTF-8') as file:
                for line in file:
                    menu_options.append(line.strip())
                return menu_options
        except FileNotFoundError:
            print("File not found")

    def persist_alarm_data(self):
        try:
            with open("data/alarms.json", "w", encoding='UTF-8') as file:
                file.write(json.dumps(alarms))
                print(f"Alarms saved to alarms.json")
        except FileNotFoundError:
            print("File not found")

    def load_alarm_data(self):
        global alarms
        try:
            with open("data/alarms.json", "r", encoding='UTF-8') as file:
                alarms = json.load(file)
                print(f"loading previously configured alarms...")
                self.logger.debug("Loading previously configured alarms %s", alarms)
                return alarms
        except FileNotFoundError:
            print("File not found")     