"""Contains the main function to run the monitoring application"""

import  time, filemanager, utility, monitoring
from customlogger import logger
from prometheus_client import start_http_server

class App:
    """Class will handle the set up of monitoring application and run the application"""

    def __init__(self):
        self.monitor = None

    def init(self):
        """
        Sets up logger and initializes the external modules.
        These modules are combined into the monitoring application.
        """
        utils = utility.Utility()
        fm = filemanager.FileManager()
        # Initialize external modules

        self.monitor = monitoring.Monitoring(logger, utils, fm)
        time.sleep(1)

    def main(self):
        """
        Main function to run the monitoring application
        """
        self.init()
        self.monitor.run()


if __name__ == "__main__":
    start_http_server(8000,addr="0.0.0.0")
    app = App()
    app.main()
