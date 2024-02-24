import logging

# Define color codes
COLOR_RESET = "\033[0m "
COLOR_RED = "\033[91m ❌"
COLOR_GREEN = "\033[92m ✅"
COLOR_YELLOW = "\033[93m ⚠️"
COLOR_BLUE = "\033[94m 🔍"
COLOR_PURPLE = "\033[95m "

CUSTOM_LEVELS = {
    logging.INFO: COLOR_GREEN,
    logging.WARNING: COLOR_YELLOW,
    logging.DEBUG: COLOR_BLUE,
    logging.ERROR: COLOR_RED,
    logging.CRITICAL: COLOR_PURPLE,
}


def configure_logging(level: int = logging.INFO):
    print(f"Setting log level to {level}")
    logging.basicConfig(level=level)

    def color_format(self, record):
        for level_num, color in CUSTOM_LEVELS.items():
            if record.levelno == level_num:
                return f"{color} {record.levelname}{COLOR_RESET}: {record.getMessage()}"

    logging.Formatter.format = color_format
