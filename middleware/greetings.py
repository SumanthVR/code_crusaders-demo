import random
from datetime import datetime

# Expanded greeting patterns with all variations
GREETING_PATTERNS = [
    # Short forms
    r'^hi$', r'^hello$', r'^hey$', r'^hola$', r'^namaste$',
    # Time-based greetings (all variations)
    r'good\s*morning', r'good\s*evening', r'good\s*afternoon', r'good\s*night',
    r'^morning$', r'^evening$', r'^afternoon$', r'^night$',
    r'^gm$', r'^ge$', r'^ga$', r'^gn$',  # Short forms
    r'hi\s+there', r'hey\s+there'  # Multi-word
]

RESPONSES = {
    'morning': [
        "Good morning! Ready to discuss investments?",
        "Morning! What financial goals shall we tackle today?"
    ],
    'afternoon': [
        "Good afternoon! Need portfolio advice?",
        "Afternoon! Any financial questions?"
    ],
    'evening': [
        "Good evening! Want to review your investments?",
        "Evening! Need financial planning help?"
    ],
    'night': [
        "Good night! Check your portfolio tomorrow.",
        "Night! Remember to track investments."
    ],
    'default': [
        "Hello! How can I assist with finances today?",
        "Hi there! What financial topics interest you?"
    ]
}

def get_time_based_greeting():
    """Returns 'morning', 'afternoon', 'evening' or 'night'"""
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return 'morning'
    elif 12 <= current_hour < 17:
        return 'afternoon'
    elif 17 <= current_hour < 22:
        return 'evening'
    else:
        return 'night'

def is_greeting(message):
    """Enhanced greeting detection using regex patterns"""
    import re
    message = message.strip().lower()
    return any(re.search(pattern, message) for pattern in GREETING_PATTERNS)

def intercept_greetings(request):
    if request.method == 'POST' and request.path == '/chat':
        try:
            data = request.get_json()
            msg = data.get('message', '').strip()
            
            if is_greeting(msg):
                time_of_day = get_time_based_greeting()
                
                # Special responses for time-based greetings
                if any(time_word in msg.lower() for time_word in ['morning', 'evening', 'afternoon', 'night']):
                    return {
                        'response': random.choice(RESPONSES[time_of_day]),
                        'is_greeting': True
                    }
                # Default response for other greetings
                return {
                    'response': random.choice(RESPONSES['default']),
                    'is_greeting': True
                }
                
        except Exception:
            pass
    return None
