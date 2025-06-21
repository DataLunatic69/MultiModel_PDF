# chatbot/interface.py
from chatbot.main import create_supervisor_app

def get_chatbot_agent():
    """Get the initialized chatbot agent"""
    return create_supervisor_app()