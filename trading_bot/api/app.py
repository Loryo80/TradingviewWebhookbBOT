"""
Flask application for the trading bot API.
"""
import os
import json
import logging
from flask import Flask, request, jsonify, render_template

from trading_bot.utils.logger import setup_logger
from trading_bot.api.webhook_handler import webhook_handler
from trading_bot.config import settings

# Configure logging
logger = setup_logger("api.app")

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__, template_folder="templates")
    
    @app.route("/", methods=["GET"])
    def index():
        """
        Render the dashboard homepage.
        """
        return render_template("index.html", title="Trading Bot Dashboard")
    
    @app.route(settings.WEBHOOK_ENDPOINT, methods=["POST"])
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
    
    @app.route("/status", methods=["GET"])
    def status():
        """
        Get the status of the trading bot.
        """
        return jsonify({
            "status": "active",
            "version": "1.0.0",
            "scheduler_enabled": settings.ENABLE_SCHEDULER,
            "scheduler_interval": settings.SCHEDULER_INTERVAL_SECONDS
        })
    
    @app.errorhandler(404)
    def not_found(error):
        """
        Handle 404 errors.
        """
        return jsonify({
            "success": False,
            "message": "Endpoint not found"
        }), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """
        Handle 500 errors.
        """
        logger.exception("Server error")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500
    
    return app