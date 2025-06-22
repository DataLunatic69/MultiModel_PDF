import streamlit as st
from components.styles import apply_custom_styles
from components.sidebar import show_sidebar_content
from components.chat_interface import display_chat_interface
from utils.agents import initialize_chatbot

def main():
    """Main application entry point"""
    # Apply custom styles
    apply_custom_styles()
    
    # Configure page settings
    st.set_page_config(
        page_title="🤖 Document Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="📚"
    )
    
    # Initialize chatbot
    if "chat_agent" not in st.session_state:
        with st.spinner("🚀 Initializing AI Assistant..."):
            st.session_state.chat_agent = initialize_chatbot()
    
    if st.session_state.chat_agent is None:
        st.error("🚨 Chatbot failed to initialize. Please check the logs.")
        st.stop()
    
    # Layout with sidebar
    show_sidebar_content()
    
    # Main chat interface
    display_chat_interface(st.session_state.chat_agent)

if __name__ == "__main__":
    main()