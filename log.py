import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("motion")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("motion.log", maxBytes=5_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - %(filename)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

if not logger.hasHandlers():
    logger.addHandler(handler)
    
    