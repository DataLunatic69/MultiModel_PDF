from langchain_groq import ChatGroq
import os

groq_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("MODEL_NAME")


def initialize_model():
    """Initialize the language model only."""

    if not groq_api_key or not model_name:
        raise ValueError("GROQ_API_KEY and MODEL_NAME must be set in environment variables.")

    model = ChatGroq(
        model_name=model_name,
        groq_api_key=groq_api_key
    )
    print("✅ Language model initialized successfully")
    return model
