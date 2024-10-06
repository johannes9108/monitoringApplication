# Monitoring Application for the course Systemutveckling i Python

# Read Menu options from a file
import logging, filemanager, utility, monitoring, time
from datetime import datetime


app = None

## Initialization Functions
def init():
    logger = logging.getLogger(__name__)
    # Root Logger Configuration
    logging.basicConfig(level=logging.info, 
                        encoding="utf-8"
                        )
    fileHandler = logging.FileHandler(datetime.now().strftime("logs/monitoring_%d_%m_%Y_%H.log"))
    formatter = logging.Formatter('%(asctime)s_%(message)s',datefmt='%d/%m/%Y_%H:%M')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.info("Initializing Monitoring Application")
    logger.debug("Setting up logger")
    
    # Initialize external modules
    utils = utility.Utility(logger)
    fm = filemanager.FileManager(logger)
    
    global app
    monitor = monitoring.Monitoring(logger, utils, fm)
    app = monitor
    time.sleep(1)
        
def main():
    init()
    app.run()
main()