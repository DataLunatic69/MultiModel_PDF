from typing import Optional, Any
from utils.logging import logger
import streamlit as st

def initialize_chatbot() -> Optional[Any]:
    """Initialize the chatbot agent with proper error handling"""
    try:
        from chatbot.interface import get_chatbot_agent
        return get_chatbot_agent()
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        st.error(f"Failed to import required modules: {str(e)}")
    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        st.error(f"Failed to initialize chatbot: {str(e)}")
    return None