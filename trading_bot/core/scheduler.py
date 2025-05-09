"""
Trading scheduler for automated market evaluation and trading.
"""
import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from trading_bot.utils.logger import setup_logger
from trading_bot.config import settings

# Configure logging
logger = setup_logger("core.scheduler")

class TradingScheduler:
    """
    Scheduler for automated trading operations.
    """
    
    def __init__(self, disable_notifications=False):
        """
        Initialize the trading scheduler.
        
        Args:
            disable_notifications (bool): Whether to disable notifications
        """
        self.interval = settings.SCHEDULER_INTERVAL_SECONDS
        self.disable_notifications = disable_notifications
        
        # Initialize scheduler
        self.scheduler = BackgroundScheduler()
        
        # Set up scheduled jobs
        self._setup_jobs()
        
        logger.info(f"Trading scheduler initialized (interval: {self.interval}s)")
    
    def start(self):
        """
        Start the scheduler.
        """
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Trading scheduler started")
    
    def stop(self):
        """
        Stop the scheduler.
        """
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Trading scheduler stopped")
    
    def _setup_jobs(self):
        """
        Set up scheduled jobs.
        """
        # Add market evaluation job
        self.scheduler.add_job(
            self._evaluate_market,
            IntervalTrigger(seconds=self.interval),
            id="market_evaluation",
            replace_existing=True
        )
        
        # Add daily reset job (midnight)
        self.scheduler.add_job(
            self._daily_reset,
            trigger="cron",
            hour=0,
            minute=0,
            id="daily_reset",
            replace_existing=True
        )
    
    def _evaluate_market(self):
        """
        Evaluate the market and execute trades if needed.
        """
        try:
            now = datetime.datetime.now()
            
            # Check if trading is allowed currently
            if not self._is_trading_allowed(now):
                return
            
            logger.debug("Evaluating market conditions")
            
            # TODO: Implement market evaluation and trading logic
            # This is a placeholder for the actual market evaluation
            
        except Exception as e:
            logger.exception(f"Error during market evaluation: {str(e)}")
    
    def _daily_reset(self):
        """
        Reset daily counters and perform end-of-day operations.
        """
        try:
            logger.info("Performing daily reset")
            
            # TODO: Implement daily reset logic
            # This is a placeholder for actual reset logic
            
        except Exception as e:
            logger.exception(f"Error during daily reset: {str(e)}")
    
    def _is_trading_allowed(self, current_time):
        """
        Check if trading is allowed at the current time.
        
        Args:
            current_time (datetime): Current time
            
        Returns:
            bool: True if trading is allowed, False otherwise
        """
        # Check if it's a weekend (Saturday=5, Sunday=6)
        is_weekend = current_time.weekday() >= 5
        
        if is_weekend and not settings.ALLOW_WEEKEND_TRADING:
            logger.debug("Trading not allowed on weekends")
            return False
        
        # Parse trading hours
        try:
            start_hour, start_minute = map(int, settings.TRADING_HOURS_START.split(":"))
            end_hour, end_minute = map(int, settings.TRADING_HOURS_END.split(":"))
            
            trading_start = current_time.replace(
                hour=start_hour, 
                minute=start_minute, 
                second=0, 
                microsecond=0
            )
            
            trading_end = current_time.replace(
                hour=end_hour, 
                minute=end_minute, 
                second=0, 
                microsecond=0
            )
            
            # Handle overnight trading hours
            if trading_end < trading_start:
                # End time is on the next day
                if current_time < trading_start and current_time > trading_end:
                    logger.debug("Outside of trading hours")
                    return False
            else:
                # Regular trading hours
                if current_time < trading_start or current_time > trading_end:
                    logger.debug("Outside of trading hours")
                    return False
            
        except ValueError:
            logger.warning("Invalid trading hours format in settings")
            # Default to allowing trading if the format is invalid
        
        return True