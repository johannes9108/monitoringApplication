import logging
from datetime import datetime

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
