import logging
from colorama import Fore, Style

class CustomFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Style.BRIGHT + Fore.CYAN,
        logging.INFO: Fore.BLUE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Style.BRIGHT + Fore.RED
    }
    RESET = Style.RESET_ALL

    def format(self, record):
        log_fmt = self.COLORS.get(record.levelno, "") + '%(asctime)s - %(levelname)s - %(message)s' + self.RESET
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Basic logger config
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(CustomFormatter())

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("runtime/app.log"),
        handler
    ]
)

logger = logging.getLogger(__name__)
