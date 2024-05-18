from logger import CustomLogger
import numpy as np
import random
import string

def random_string(length=5):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase 
    return ''.join(random.choice(letters) for i in range(length))

logger = CustomLogger(level="DEBUG", ignore=["/health", "Press CTRL+C to quit"], include_date=True, include_level=False)

logger.spam("This is a spam message.")
logger.debug("This is a debug message.")

logger.verbose("This is a verbose message.")
logger.info("This is an info message.")
logger.notice("This is a notice message.")
logger.warning("This is a warning message.")
logger.success("This is a success message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")

x = [np.random.randint(1, 10) for i in range(5)]
y = {i: random_string(5) for i in range(5)}
logger.info(x)
logger.error(y)

