"""Contains the main function to run the monitoring application"""

from datetime import datetime
import logging, time, filemanager, utility, monitoring
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

        logger = logging.getLogger(__name__)
        # Root Logger Configuration
        logging.basicConfig(level=logging.INFO, encoding="utf-8")
        fileHandler = logging.FileHandler(
            datetime.now().strftime("logs/monitoring_%d_%m_%Y_%H.log")
        )
        formatter = logging.Formatter(
            "%(asctime)s_%(message)s", datefmt="%d/%m/%Y_%H:%M:%S"
        )
        fileHandler.setFormatter(formatter)
        for handler in logging.root.handlers[:]:
            if isinstance(handler, logging.StreamHandler):
                logging.root.removeHandler(handler)
        logger.addHandler(fileHandler)
        logger.info("Initializing_Monitoring_Application")
        logger.debug("Setting_up_logger")

        # Initialize external modules
        utils = utility.Utility(logger)
        fm = filemanager.FileManager(logger, utils)
    
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
