import logging
import os
import pathlib
import sys
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("stack_machine")

log_file_path = '../../'

if not os.path.exists(log_file_path + "cpu.log"):
    pathlib.Path(log_file_path).mkdir(parents=True, exist_ok=True)
    with open(log_file_path + "cpu.log", "a") as log_file:
        pass

# handler = RotatingFileHandler(log_file_path + "cpu.log", maxBytes=1024 * 1024, backupCount=5)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s.%(msecs)03d  - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))


logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
