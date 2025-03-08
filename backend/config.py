import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys and service configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# File storage configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
MAX_CONTENT_LENGTH = int(
    os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # Default 16MB

# LLM configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 1000))

# Marker configuration
MARKER_USE_LLM = os.getenv(
    "MARKER_USE_LLM", "False").lower() in ("true", "1", "t")
MARKER_FORCE_OCR = os.getenv(
    "MARKER_FORCE_OCR", "False").lower() in ("true", "1", "t")
TORCH_DEVICE = os.getenv("TORCH_DEVICE", "cuda" if os.getenv(
    "CUDA_VISIBLE_DEVICES") else "cpu")

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
