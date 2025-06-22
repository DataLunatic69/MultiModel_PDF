import streamlit as st
import time
from typing import Dict, Any
from utils.logging import logger
from .response_utils import get_response

def display_chat_interface(agent):
    """Display the enhanced chat interface"""
    # Header with improved styling
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">📚 Multimodal Document Assistant</h1>
        <p style="color: #666; font-size: 1.1rem;">Ask intelligent questions about your processed documents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    display_chat_messages()
    
    # Handle user input
    handle_user_input(agent)

def display_chat_messages():
    """Display all chat messages in the conversation"""
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            display_user_message(message["content"])
        else:
            display_assistant_message(message)

def display_user_message(content: str):
    """Display a user message with styling"""
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 1rem 1rem 0.3rem 1rem; 
                    max-width: 70%; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <strong>You:</strong><br>{content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_assistant_message(message: Dict[str, Any]):
    """Display an assistant message with metadata"""
    with st.container():
        if "agent_calls" in message and message["agent_calls"]:
            display_agent_metadata(message)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    color: white; padding: 1rem; border-radius: 0.3rem 0.3rem 1rem 0.3rem; 
                    margin: 0 0 1rem 0; max-width: 85%;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        
        st.markdown(message["content"])
        st.markdown("</div>", unsafe_allow_html=True)

def display_agent_metadata(message: Dict[str, Any]):
    """Display agent workflow and token usage metadata"""
    agent_workflow = ' → '.join([call['agent'] for call in message['agent_calls']])
    total_tokens = message.get("total_tokens", 0)
    responding_agent = message.get("responding_agent", "Unknown")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                color: white; padding: 0.75rem 1rem 0.5rem 1rem; 
                border-radius: 1rem 1rem 0.3rem 0.3rem; 
                margin: 1rem 0 0 0; max-width: 85%;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <strong>🤖 Assistant Response</strong><br>
        <div style="background: rgba(255,255,255,0.15); padding: 0.5rem; 
                    border-radius: 0.5rem; margin-top: 0.5rem; font-size: 0.85rem;">
            <strong>🔧 Agent Workflow:</strong> {agent_workflow}<br>
            <strong>📊 Token Usage:</strong> {total_tokens} total tokens<br>
            <strong>🎯 Responding Agent:</strong> {responding_agent}
        </div>
    </div>
    """, unsafe_allow_html=True)

def handle_user_input(agent):
    """Handle user input and generate responses"""
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    input_col1, input_col2 = st.columns([6, 1])
    
    with input_col1:
        user_input = st.text_input(
            "Ask your question:",
            placeholder="e.g., What is query decomposition? How do tables relate to the main content?",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with input_col2:
        send_button = st.button("Send 📤", type="primary", use_container_width=True)
    
    if send_button and user_input.strip():
        process_user_input(agent, user_input.strip())

def process_user_input(agent, prompt: str):
    """Process user input and generate response"""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show thinking indicator
    with st.spinner("🤔 Analyzing your question..."):
        time.sleep(0.5)
        response = get_response(agent, prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response["content"],
        "agent_calls": response.get("agent_calls", []),
        "total_tokens": response.get("total_tokens", 0),
        "responding_agent": response.get("responding_agent", None)
    })
    
    # Clear input and rerun to show new messages
    st.rerun()