from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
from models.gemini_service import GeminiService
from models.financial_data import FinancialDataService
from utils.helpers import format_response
from utils.prompts import get_financial_prompt
from middleware.greetings import intercept_greetings
import random
import config

# Load environment variables
load_dotenv()

# Debugging: Print environment variables
print("🔹 GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
print("🔹 FLASK_ENV:", os.getenv("FLASK_ENV"))
print("🔹 SECRET_KEY:", os.getenv("SECRET_KEY"))

# Ensure API key is loaded
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("🚨 GOOGLE_API_KEY is missing! Check your .env file.")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# Enable CORS
CORS(app)

# Initialize services
gemini_service = GeminiService(api_key=GOOGLE_API_KEY)
financial_data = FinancialDataService()

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests with greeting interception"""
    # ===== NEW GREETING INTERCEPTION =====
    greeting_response = intercept_greetings(request)
    if greeting_response:
        return jsonify(greeting_response)
    # ===== END OF NEW CODE =====

    # ===== ORIGINAL CODE (100% UNCHANGED) =====
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        app.logger.debug(f"🔹 Received message: {user_message}")

        if not user_message:
            return jsonify({'response': 'Please enter a valid financial question.'})

        if financial_data.needs_market_data(user_message):
            market_context = financial_data.get_relevant_data(user_message)
            prompt = get_financial_prompt(user_message, market_context)
        else:
            prompt = get_financial_prompt(user_message)

        app.logger.debug(f"📝 Prompt sent to Gemini: {prompt}")
        
        response = gemini_service.generate_response(prompt)
        
        app.logger.debug(f"🤖 AI Response: {response}")

        formatted_response = format_response(response)
        return jsonify({'response': formatted_response})

    except Exception as e:
        app.logger.error(f"⚠️ Error processing chat: {str(e)}", exc_info=True)
        return jsonify({'response': 'Sorry, I encountered an error.'}), 500
    # ===== END OF ORIGINAL CODE =====

@app.route('/search-investments', methods=['POST'])
def search_investments():
    """Search for investment products based on criteria"""
    try:
        data = request.json
        criteria = data.get('criteria', {})
        
        # Get investment recommendations
        results = financial_data.search_investments(criteria)
        
        return jsonify({'results': results})
    
    except Exception as e:
        app.logger.error(f"⚠️ Error searching investments: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to search for investments'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
