#!/usr/bin/env python
"""
Main application entry point.
This file serves as a compatibility layer with the original application.
For new functionality, use `python -m trading_bot` instead.
"""
import os
import sys
import json
import logging
import warnings
from flask import Flask, request, jsonify

# Add the project root to the system path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import new trading bot modules
from trading_bot.utils.logger import setup_logger
from trading_bot.api.webhook_handler import webhook_handler

# Configure logging
logger = setup_logger("app")

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Create Flask application
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle webhook requests from signal sources.
    """
    try:
        # Parse the webhook payload
        if request.is_json:
            webhook_data = request.get_json()
        else:
            try:
                webhook_data = json.loads(request.data)
            except json.JSONDecodeError:
                # Try to parse as form data for backward compatibility
                webhook_data = {
                    "passphrase": request.form.get("passphrase", ""),
                    "ticker": request.form.get("ticker", ""),
                    "strategy": {
                        "order_action": request.form.get("order_action", ""),
                        "order_price": float(request.form.get("order_price", 0))
                    }
                }
            
        # Process the webhook request
        logger.info(f"Received webhook: {webhook_data}")
        result = webhook_handler.process_request(webhook_data)
        
        # Return the result
        return jsonify(result)
        
    except Exception as e:
        error_message = f"Error handling webhook request: {str(e)}"
        logger.exception(error_message)
        
        return jsonify({
            "success": False,
            "message": error_message
        })

if __name__ == "__main__":
    # Print startup message
    print("Starting Trading Bot (Legacy Mode)")
    print("For full functionality, use: python -m trading_bot")
    
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=False)