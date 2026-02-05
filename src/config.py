import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar .env desde el directorio raíz
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "15"))

# Chatbot Configuration
CHATBOT_MAX_CONTEXT_MESSAGES = int(os.getenv("CHATBOT_MAX_CONTEXT_MESSAGES", "10"))
CHATBOT_TIMEOUT = int(os.getenv("CHATBOT_TIMEOUT", "30"))

# Context Manager
MAX_TOKENS = 4000
WINDOW_MESSAGES = CHATBOT_MAX_CONTEXT_MESSAGES

# Application Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate required settings
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no configurada en .env")
