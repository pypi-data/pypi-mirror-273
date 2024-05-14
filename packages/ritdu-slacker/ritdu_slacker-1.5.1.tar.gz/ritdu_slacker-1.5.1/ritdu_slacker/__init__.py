import importlib.metadata
import logging
import sys

from signal import signal, SIGINT


metadata = importlib.metadata.metadata(__package__)

TOOL_NAME = metadata["Name"]
TOOL_VERSION = metadata["Version"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logging.basicConfig(
    format=f"[%(asctime)s] {TOOL_NAME} [%(levelname)s] %(funcName)s %(lineno)d: %(message)s"
)


def sigint_handler(signal_received, frame):
    """Handle SIGINT or CTRL-C and exit gracefully"""
    logger.warning("SIGINT or CTRL-C detected. Exiting gracefully")
    sys.exit(0)


signal(SIGINT, sigint_handler)
