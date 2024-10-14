import os, time
from customlogger import logger as importLogger


class UI:
    @staticmethod
    def init():
        """
        Reading menu options from txt-file
        """
        menuOptions = []
        try:
            with open("data/menuOptions.txt", "r", encoding="UTF-8") as file:
                for line in file:
                    menuOptions.append(line.strip())
                return menuOptions
        except FileNotFoundError:
            importLogger.error("File not found")
    menuOptions = init()
    def __init__(self):
        pass
    @staticmethod
    def displayMenu(menu=None):
        """
        Displays the main menu
        """
        if menu == None:
            UI.displayStartFrame("Monitoring Application")
            for index, option in enumerate(UI.menuOptions):
                print(f"{index+1} {option}")
            print(f"{len(UI.menuOptions)+1} Exit\n")
        else:
            for index, option in enumerate(menu):
                print(f"{index+1} {option}")
        UI.displayEndFrame()
    @staticmethod
    def displayStartFrame(title):
        """
        Displays the start frame with a title of the CLI
        """
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{title}\n{'-'*len(title)}", end="\n\n")
    @staticmethod
    def displayEndFrame( halt=False):
        """
        Displays the end frame with a prompt to continue depending on the halt parameter
        """
        time.sleep(.5)
        if halt == True:
            input("Press Enter to continue...")
            os.system("cls" if os.name == "nt" else "clear")
    @staticmethod
    def displayAlarms(alarms, subMenu=False):
        """
        Displays the alarms
        """
        UI.displayStartFrame("Alarms")
        count = 0
        for i in range(len(alarms["cpuAlarms"])):
            count += 1
            print(f"{count}. CPU Alarm {alarms['cpuAlarms'][i]}%")
        for i in range(len(alarms["memoryAlarms"])):
            count += 1
            print(f"{count}. Memory Alarm {alarms['memoryAlarms'][i]}%")
        for i in range(len(alarms["diskAlarms"])):
            count += 1
            print(f"{count}. Disk Alarm {alarms['diskAlarms'][i]}%")
        if not subMenu:
            input("Press Enter to return to main menu...")
        UI.displayEndFrame()
    @staticmethod
    def input(text):
        """
        Displays the input prompt
        """
        return input(text)
        
    @staticmethod
    def print(*texts,sep=" ", end="\n"):
        """
        Displays the text
        """
        
        if len(texts) == 1:
            print(texts[0],sep=sep,end=end)
        else: 
            for msg in texts:
                print(msg,sep=sep,end=end)