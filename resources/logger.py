import datetime
import logging
import os
from config import OUTPUT_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file handler and set its level and formatter
today = datetime.datetime.now().strftime("%Y-%m-%d")
log_path = os.path.join(OUTPUT_DIR, f'log_{today}.log')
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Uncomment to create a console handler and set its level and formatter
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
#logger.addHandler(console_handler)