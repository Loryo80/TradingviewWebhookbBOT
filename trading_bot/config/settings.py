"""
Settings configuration for the trading bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MetaTrader5 settings
MT5_USERNAME = os.getenv("MT5_USERNAME", "")
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")

# Webhook settings
WEBHOOK_PASSPHRASE = os.getenv("WEBHOOK_PASSPHRASE", "")
WEBHOOK_ENDPOINT = os.getenv("WEBHOOK_ENDPOINT", "/webhook")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 5000))
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")

# Notification settings
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "True").lower() in ("true", "1", "yes")

# Scheduler settings
SCHEDULER_INTERVAL_SECONDS = int(os.getenv("SCHEDULER_INTERVAL_SECONDS", 15))
ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "True").lower() in ("true", "1", "yes")

# Trading settings
RISK_PERCENTAGE = float(os.getenv("RISK_PERCENTAGE", 1.0))
REWARD_PERCENTAGE = float(os.getenv("REWARD_PERCENTAGE", 2.0))
ATR_PERIOD = int(os.getenv("ATR_PERIOD", 14))
ATR_MULTIPLIER = float(os.getenv("ATR_MULTIPLIER", 2.0))

# Risk management settings
MAX_DAILY_LOSS_PERCENTAGE = float(os.getenv("MAX_DAILY_LOSS_PERCENTAGE", 5.0))
ALLOW_WEEKEND_TRADING = os.getenv("ALLOW_WEEKEND_TRADING", "False").lower() in ("true", "1", "yes")
TRADING_HOURS_START = os.getenv("TRADING_HOURS_START", "00:00")
TRADING_HOURS_END = os.getenv("TRADING_HOURS_END", "23:59")

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/trading_bot.log")

# Advanced position management
ENABLE_BREAKEVEN = os.getenv("ENABLE_BREAKEVEN", "True").lower() in ("true", "1", "yes")
BREAKEVEN_TRIGGER_PERCENTAGE = float(os.getenv("BREAKEVEN_TRIGGER_PERCENTAGE", 0.5))
ENABLE_TRAILING_STOP = os.getenv("ENABLE_TRAILING_STOP", "False").lower() in ("true", "1", "yes")
TRAILING_STOP_TRIGGER_PERCENTAGE = float(os.getenv("TRAILING_STOP_TRIGGER_PERCENTAGE", 0.7))
TRAILING_STOP_STEP_PERCENTAGE = float(os.getenv("TRAILING_STOP_STEP_PERCENTAGE", 0.2))