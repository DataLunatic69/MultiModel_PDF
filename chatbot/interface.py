from chatbot.main import create_supervisor_app

def get_chatbot_agent():
    """Get initialized agent with error handling"""
    try:
        return create_supervisor_app()
    except Exception as e:
        raise RuntimeError(f"Agent initialization failed: {str(e)}")