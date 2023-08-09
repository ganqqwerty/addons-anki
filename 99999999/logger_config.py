import logging
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the full path for the log file
log_path = os.path.join(current_dir, 'intellifiller.log')

# Clear the log file
with open(log_path, 'w'):
    pass

logger = logging.getLogger("addon.IntelliFiller")

# Create a handler to output logs to a file in the same directory as the script
handler = logging.FileHandler(log_path, 'a', 'utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s in %(filename)s:%(lineno)d', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
