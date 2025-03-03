import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys and service configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
# PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# File storage configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
MAX_CONTENT_LENGTH = int(
    os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # Default 16MB

# LLM configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 1000))

# MarkItDown configuration
MARKITDOWN_ENABLE_PLUGINS = os.getenv(
    "MARKITDOWN_ENABLE_PLUGINS", "False").lower() in ("true", "1", "t")
MARKITDOWN_DOCINTEL_ENDPOINT = os.getenv("MARKITDOWN_DOCINTEL_ENDPOINT")

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
