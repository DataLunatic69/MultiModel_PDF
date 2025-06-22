from chatbot.main import create_supervisor_app
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_chatbot_agent():
    """Get initialized agent with enhanced debugging"""
    try:
        logger.debug("Initializing supervisor app...")
        agent = create_supervisor_app()
        
        # Debug the agent structure
        logger.debug(f"Agent type: {type(agent)}")
        if hasattr(agent, 'model'):
            logger.debug("Agent has model configured")
        else:
            logger.warning("Agent missing model configuration")
            
        return agent
    except Exception as e:
        logger.error(f"Agent initialization failed: {str(e)}", exc_info=True)
        raise RuntimeError(f"Agent initialization failed: {str(e)}")