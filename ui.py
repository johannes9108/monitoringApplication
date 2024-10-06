import os, time

class UI:
    def __init__(self, logger, monitor):
        self.monitor = monitor
        self.menu_options = []
        self.logger = logger
        logger.info("Initializing UI")
    def run(self):
        self.menu_options = self.monitor.fm.read_menu_options()
        while True:
            self.display_menu()
            try: 
                choice = int(input("Enter choice: "))
                if choice == 1:
                    self.monitor.start_monitoring()
                elif choice == 2:
                    self.monitor.list_active_monitoring(True)
                elif choice == 3:
                    self.monitor.create_alarm()
                elif choice == 4:
                    self.monitor.remove_alarm()
                elif choice == 5:
                    self.monitor.display_alarms()
                elif choice == 6:
                    self.monitor.start_monitoring_mode()
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