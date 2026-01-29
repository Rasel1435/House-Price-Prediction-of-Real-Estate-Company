import logging
import os
from datetime import datetime

def configure_logger(name: str = "ML_Pipeline"):
    """
    Sets up a professional logger that outputs to both console and file.
    """
    # Create a 'logs' directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define the log file name with today's date
    log_filename = f"{datetime.now().strftime('%Y-%m-%d')}_pipeline.log"
    log_path = os.path.join(log_dir, log_filename)

    # Create a logger instance
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, don't add more (prevents duplicate logs)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Create Format (Professional timestamp and level)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # Console Handler (Prints to your terminal)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler (Saves to logs/ folder)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger