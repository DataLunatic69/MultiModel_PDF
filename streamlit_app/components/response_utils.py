from typing import Dict, Any, List
from utils.logging import logger

def extract_response_with_metadata(response: Dict[str, Any]) -> Dict[str, Any]:
    """Extract the meaningful final response with agent and token metadata"""
    try:
        raw_response = response.get("raw_response", {})
        
        if isinstance(raw_response, dict) and "messages" in raw_response:
            messages = raw_response["messages"]
            return process_messages(messages)
        
        return create_fallback_response(response)
        
    except Exception as e:
        logger.error(f"Error extracting response: {str(e)}")
        return create_error_response(str(e))

def process_messages(messages: List[Dict]) -> Dict[str, Any]:
    """Process agent messages to extract relevant information"""
    agent_calls = []
    total_tokens = 0
    best_content = ""
    best_length = 0
    responding_agent = None
    
    for message in messages:
        # Handle both dict and object-style messages
        if isinstance(message, dict):
            content = message.get("content", "")
            agent_name = message.get("name")
            metadata = message.get("response_metadata", {})
        else:
            content = getattr(message, "content", "")
            agent_name = getattr(message, "name", None)
            metadata = getattr(message, "response_metadata", {})
        
        # Process agent and token information
        if agent_name:
            tokens = metadata.get("token_usage", {}).get("total_tokens", 0)
            total_tokens += tokens
            
            if tokens > 0:
                agent_calls.append({
                    'agent': agent_name,
                    'tokens': tokens
                })
        
        # Process message content
        if should_include_content(content):
            current_length = len(content)
            if current_length > best_length:
                best_content = content
                best_length = current_length
                responding_agent = agent_name
    
    return {
        'content': best_content if best_content else "No meaningful response found",
        'agent_calls': agent_calls,
        'total_tokens': total_tokens,
        'responding_agent': responding_agent
    }

def get_token_count(message: Dict) -> int:
    """Extract token count from message metadata"""
    if message.get("usage_metadata"):
        return message["usage_metadata"].get("total_tokens", 0)
    elif message.get("response_metadata") and message["response_metadata"].get("token_usage"):
        return message["response_metadata"]["token_usage"].get("total_tokens", 0)
    return 0

def should_include_content(content: str) -> bool:
    """Determine if content should be included in final response"""
    skip_phrases = [
        'Transferring', 'Successfully transferred', 'I will now respond directly',
        'The query has been successfully processed', 'Now that the query has been processed',
        'Since the response has been transferred back', 'To confirm, the original query was',
        'To summarize, the user asked'
    ]
    return (content and 
            not any(phrase in content for phrase in skip_phrases) and
            len(content) > 100)

def create_fallback_response(response: Dict) -> Dict[str, Any]:
    """Create a fallback response when message processing fails"""
    return {
        'content': response.get("content", "No meaningful response found"),
        'agent_calls': [],
        'total_tokens': 0,
        'responding_agent': None
    }

def create_error_response(error: str) -> Dict[str, Any]:
    """Create an error response"""
    return {
        'content': f"Error processing response: {error}",
        'agent_calls': [],
        'total_tokens': 0,
        'responding_agent': None
    }

def format_response(content: str) -> str:
    """Format the response content for better readability"""
    if not content:
        return "No response available"
    
    # Clean up the content
    content = content.strip()
    
    # Remove any remaining coordination messages that might have slipped through
    lines = content.split('\n')
    filtered_lines = []
    
    for line in lines:
        line = line.strip()
        if (line and 
            not any(phrase in line for phrase in [
                'Successfully transferred',
                'Transferring back to',
                'I will now respond directly',
                'The query has been successfully processed',
                'To confirm, the original query was'
            ])):
            filtered_lines.append(line)
    
    content = '\n'.join(filtered_lines).strip()
    
    # Split into paragraphs for better formatting
    paragraphs = content.split('\n\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if para:
            # Handle numbered lists
            if any(para.startswith(f"{i}.") for i in range(1, 10)):
                lines = para.split('\n')
                formatted_lines = []
                for line in lines:
                    line = line.strip()
                    if any(line.startswith(f"{i}.") for i in range(1, 10)):
                        number_part = line.split('.', 1)
                        if len(number_part) > 1:
                            formatted_lines.append(f"**{number_part[0]}.**{number_part[1]}")
                        else:
                            formatted_lines.append(line)
                    else:
                        formatted_lines.append(line)
                formatted_paragraphs.append('\n'.join(formatted_lines))
            
            # Handle bullet points
            elif para.startswith('*'):
                lines = para.split('\n')
                formatted_lines = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('*'):
                        formatted_lines.append(f"• **{line[1:].strip()}**" if len(line[1:].strip()) < 100 else f"• {line[1:].strip()}")
                    else:
                        formatted_lines.append(line)
                formatted_paragraphs.append('\n'.join(formatted_lines))
            else:
                # Regular paragraphs - make first sentence bold if it's a definition
                sentences = para.split('. ')
                if len(sentences) > 1 and len(sentences[0]) < 200:
                    formatted_para = f"**{sentences[0]}.**"
                    if len(sentences) > 1:
                        formatted_para += f" {'. '.join(sentences[1:])}"
                    formatted_paragraphs.append(formatted_para)
                else:
                    formatted_paragraphs.append(para)
    
    return '\n\n'.join(formatted_paragraphs)

def get_response(agent, prompt: str) -> Dict[str, Any]:
    """Get response from chatbot with enhanced debugging and formatting"""
    try:
        logger.debug(f"Invoking agent with prompt: {prompt}")
        
        # Prepare the input message structure
        from langchain.schema import HumanMessage
        messages = [{"role": "user", "content": prompt}]
        
        # Invoke the agent
        response = agent.invoke({"messages": messages})
        
        logger.debug(f"Raw agent response type: {type(response)}")
        
        # Create response dict
        response_dict = {
            "success": True,
            "content": "Processing...",
            "raw_response": response
        }
        
        # Extract and format the meaningful response with metadata
        response_data = extract_response_with_metadata(response_dict)
        formatted_content = format_response(response_data['content'])
        
        return {
            "success": True,
            "content": formatted_content,
            "agent_calls": response_data['agent_calls'],
            "total_tokens": response_data['total_tokens'],
            "responding_agent": response_data['responding_agent'],
            "raw_response": response
        }
        
    except Exception as e:
        logger.error(f"Error in get_response: {str(e)}", exc_info=True)
        return {
            "success": False,
            "content": f"❌ **Error occurred:** {str(e)}",
            "agent_calls": [],
            "total_tokens": 0,
            "responding_agent": None,
            "raw_response": None
        }