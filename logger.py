import logging
import sys


def configure_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('extract_accounting.log', mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )
