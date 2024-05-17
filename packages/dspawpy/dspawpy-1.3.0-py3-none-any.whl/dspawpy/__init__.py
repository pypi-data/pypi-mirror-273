# -*- coding: utf-8 -*-
__version__ = "1.3.0"

from loguru import logger
import os
import sys

# check python version must be 3.6+
assert sys.version_info >= (3, 6)

logger.remove()
level = os.getenv("dspawpy_log_level")
if level is None:  # default to simulate no log
    level = "concise"
    logger.add(
        sys.stderr,
        # format="<green>{time:MM-DD HH:mm:ss:SSS}</green> | <level>{message}</level>",
        format="{message}",
    )
else:
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:MM-DD HH:mm:ss:SSS}</green> | <level>{message}</level>",
    )

logger.add(
    ".dspawpy.log",
    level="DEBUG",
    rotation="1 day",
    retention="1 week",
    compression="zip",
)
