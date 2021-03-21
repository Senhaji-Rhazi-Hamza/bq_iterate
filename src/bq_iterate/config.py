import sys
import logging


FORMAT = "%(asctime)s - (%(name)s) - %(levelname)s - %(message)s"

logging.basicConfig(format=FORMAT)

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)
for handler in logger.handlers:
    logger.removeHandler(handler)

logger.addHandler(handler)

RETRY_CONF = {
    "wait_multiplier": 2,
    "wait_min": 4,
    "wait_max": 40,
    "stop_after_attempt": 6,
}
