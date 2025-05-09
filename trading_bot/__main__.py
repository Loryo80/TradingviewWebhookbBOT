#!/usr/bin/env python
"""
Main entry point for the trading bot package.
"""
import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add application modules
from trading_bot.utils.logger import setup_logger
from trading_bot.api.app import create_app
from trading_bot.core.scheduler import TradingScheduler

# Setup logging
logger = setup_logger("trading_bot")

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Trading Bot")
    parser.add_argument(
        "--no-scheduler", 
        action="store_true", 
        help="Disable the scheduler"
    )
    parser.add_argument(
        "--no-notifications", 
        action="store_true", 
        help="Disable notifications"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.getenv("WEBHOOK_PORT", 5000)),
        help="Port for the webhook server"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default=os.getenv("WEBHOOK_HOST", "0.0.0.0"),
        help="Host for the webhook server"
    )
    
    return parser.parse_args()

def main():
    """
    Main entry point for the trading bot.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Print banner
    print("=" * 50)
    print("TRADING VIEW WEBHOOK BOT")
    print("=" * 50)
    print(f"Version: {trading_bot.__version__}")
    print(f"Author: {trading_bot.__author__}")
    print("=" * 50)
    
    # Create Flask application
    app = create_app()
    
    # Start the scheduler if enabled
    if not args.no_scheduler and os.getenv("ENABLE_SCHEDULER", "True").lower() in ("true", "1", "yes"):
        logger.info("Starting scheduler")
        scheduler = TradingScheduler(disable_notifications=args.no_notifications)
        scheduler.start()
    else:
        logger.info("Scheduler disabled")
    
    # Start the Flask application
    logger.info(f"Starting webhook server at {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    # Add the project root to the system path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # Fix circular import
    import trading_bot
    
    main()