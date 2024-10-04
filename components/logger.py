import logging

# basic logger config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("runtime/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)