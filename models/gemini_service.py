import google.generativeai as genai
import logging
from config import GEMINI_MODEL, MAX_RESPONSE_TOKENS, SHORT_RESPONSE_TOKENS

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google's Gemini model"""

    def __init__(self, api_key):
        """Initialize the Gemini service with API key"""
        if not api_key:
            raise ValueError("🚨 GOOGLE_API_KEY is missing! Check your .env file.")

        self.api_key = api_key
        self.configure_api()

        try:
            self.model = genai.GenerativeModel(GEMINI_MODEL)
            logger.info("✅ Gemini model loaded successfully!")
        except Exception as e:
            logger.error(f"⚠️ Error initializing Gemini model: {str(e)}")
            self.model = None

        self.chat_session = None

    def configure_api(self):
        """Configure the Gemini API with credentials"""
        try:
            genai.configure(api_key=self.api_key)
            logger.info("✅ Gemini API configured successfully!")
        except Exception as e:
            logger.error(f"⚠️ Error configuring Gemini API: {str(e)}")

    def start_chat(self):
        """Start a new chat session"""
        try:
            if not self.model:
                raise ValueError("🚨 Gemini model is not initialized!")

            self.chat_session = self.model.start_chat(
                history=[],
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": MAX_RESPONSE_TOKENS
                }
            )
            logger.info("✅ Chat session started!")
        except Exception as e:
            logger.error(f"⚠️ Error starting chat session: {str(e)}")

    def _is_simple_prompt(self, prompt):
        """Check if prompt is a simple greeting/short message"""
        return len(prompt.split('\n')) <= 3 and "Respond briefly" in prompt

    def generate_response(self, prompt):
        """Generate a response from the model using the provided prompt"""
        try:
            if not self.model:
                raise ValueError("🚨 Gemini model is not initialized!")

            logger.debug(f"📝 Prompt sent to Gemini: {prompt}")

            # Determine response length based on prompt type
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": (
                    SHORT_RESPONSE_TOKENS if self._is_simple_prompt(prompt) 
                    else MAX_RESPONSE_TOKENS
                )
            }

            # Generate the response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            if response and hasattr(response, "text"):
                logger.debug(f"🤖 Gemini response: {response.text}")
                return response.text
            else:
                logger.warning("⚠️ Gemini response is empty!")
                return "I'm sorry, I couldn't generate a response. Please try again."

        except Exception as e:
            logger.error(f"⚠️ Error generating response: {str(e)}")
            return "I'm sorry, I'm having trouble responding right now. Please try again later."

    def generate_direct_response(self, prompt):
        """Generate a one-time response without chat history"""
        try:
            if not self.model:
                raise ValueError("🚨 Gemini model is not initialized!")

            logger.debug(f"📝 Direct Prompt: {prompt}")
            
            # Use default length for direct responses
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": MAX_RESPONSE_TOKENS
                }
            )

            if response and hasattr(response, "text"):
                logger.debug(f"🤖 Direct AI Response: {response.text}")
                return response.text
            else:
                logger.warning("⚠️ Direct Gemini response is empty!")
                return "I'm sorry, I couldn't generate a response. Please try again."

        except Exception as e:
            logger.error(f"⚠️ Error in generate_direct_response: {str(e)}")
            return "I'm sorry, I'm having trouble responding right now. Please try again later."

    def reset_chat(self):
        """Reset the chat session"""
        logger.info("🔄 Chat session reset!")
        self.chat_session = None
