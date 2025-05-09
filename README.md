# Trading Automation System

A real-time trading automation system that integrates external signal sources, evaluates trading logic on a schedule, and manages execution through a broker API (MetaTrader 5).

## Features

- **Webhook Integration**: Receive trading signals from TradingView or other sources via webhooks
- **Scheduled Evaluation**: Automatically evaluate market conditions every 15 seconds
- **Position Management**: Advanced position management including breakeven and trailing stop functionality
- **Risk Management**: Time-based trading restrictions and daily loss limits
- **Notifications**: Discord notifications for trade events and errors
- **Dashboard**: Simple web dashboard for monitoring system status and open positions

## Architecture

The system is built with a modular architecture:

```
trading_bot/
├── api/               # API endpoints including webhooks
├── core/              # Core business logic
├── services/          # External service integrations
│   ├── broker/        # Broker API integration (MT5)
│   ├── market_data/   # Market data services
│   └── notifications/ # Notification services
├── utils/             # Utility functions
├── config/            # Configuration files
└── logs/              # Logging output
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/loryO80/trading-automation.git
   cd trading-automation
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure MetaTrader 5:
   - Install MetaTrader 5
   - Log in to your account

4. Create a configuration file:
   Copy `env.example` to `.env` and update the values:
   ```
   MT5_USERNAME=your_username
   MT5_PASSWORD=your_password
   MT5_SERVER=your_server
   WEBHOOK_PASSPHRASE=your_webhook_passphrase
   ```

## Usage

### Running the application

```
python -m trading_bot
```

Or use the legacy mode for backward compatibility:

```
python app.py
```

### Command line options

```
python -m trading_bot --help
```

Options:
- `--no-scheduler`: Disable the scheduler on startup
- `--no-notifications`: Disable notifications

### Accessing the dashboard

Open a web browser and navigate to [http://localhost:5000](http://localhost:5000)

### Sending signals via webhook

Send a POST request to `http://localhost:5000/webhook` with a payload like:

```json
{
    "passphrase": "your_webhook_passphrase",
    "ticker": "EURUSD",
    "strategy": {
        "order_action": "buy",
        "order_price": 1.1000
    }
}
```

## Configuration

All configuration options are available in `trading_bot/config/settings.py` and can be overridden using environment variables. Key settings:

- **MetaTrader 5**: Username, password, server
- **Webhook**: Passphrase, endpoint, port
- **Scheduler**: Interval, enabled/disabled
- **Trading**: Risk percentage, ATR period, ATR multiplier
- **Risk Management**: Max daily loss, trading hours, weekend trading
- **Position Management**: Breakeven trigger, trailing stop

## Project Structure

The important files in this project are:

- `run.py` - Simple runner script for the trading bot
- `app.py` - Legacy compatibility layer for the original webhook handler
- `trading_bot/` - Main package with all the new functionality
  - `__main__.py` - Entry point when running as a module
  - `api/app.py` - Flask application with webhook handling and dashboard
  - `core/scheduler.py` - Scheduler for real-time market evaluation
  - `services/broker/mt5_broker_service.py` - MetaTrader 5 integration
  - `services/market_data/mt5_data_service.py` - Market data service
  - `services/notifications/notification_service.py` - Notification service

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.