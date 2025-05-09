"""
Logging configuration for the trading bot.
"""
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, level=None, log_file=None):
    """
    Set up a logger with the specified name and configuration.
    
    Args:
        name (str): Name of the logger
        level (str, optional): Log level. Defaults to None (uses env var or INFO).
        log_file (str, optional): Path to log file. Defaults to None (uses env var or logs/trading_bot.log).
    
    Returns:
        logging.Logger: Configured logger
    """
    # Get log level from environment variable or use INFO as default
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Get log file from environment variable or use default
    if log_file is None:
        log_file = os.getenv("LOG_FILE", "logs/trading_bot.log")
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create file handler with rotation (10 MB max size, keep 5 backups)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger