import streamlit as st
import os
import time
import sys
import shutil
from langchain.schema import HumanMessage, AIMessage

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from root package
from utilse import process_document
from chatbot.interface import get_chatbot_agent

# Set page config
st.set_page_config(
    page_title="Multimodal PDF Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing_result" not in st.session_state:
    st.session_state.processing_result = None
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False
if "chatbot_agent" not in st.session_state:
    st.session_state.chatbot_agent = None
if "temp_files" not in st.session_state:
    st.session_state.temp_files = []

# Sidebar for document upload
with st.sidebar:
    st.title("PDF Processing")
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    
    if uploaded_file is not None:
        # Clear previous state
        st.session_state.document_processed = False
        st.session_state.messages = []
        st.session_state.processing_result = None
        
        # Save the file temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, f"uploaded_{int(time.time())}.pdf")
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Store temp file for cleanup
        st.session_state.temp_files.append(file_path)
        
        # Process document
        with st.spinner("Processing document..."):
            try:
                result = process_document(file_path)
                st.session_state.processing_result = result
                st.session_state.document_processed = True
                
                # Initialize chatbot after processing
                st.session_state.chatbot_agent = get_chatbot_agent()
                st.success("Document processed successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                st.session_state.document_processed = False

# Cleanup function
def cleanup_temp_files():
    for file_path in st.session_state.temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
    st.session_state.temp_files = []

# Register cleanup on app exit
st.session_state.cleanup = cleanup_temp_files

# Main chat interface
st.title("📄 Multimodal PDF Chatbot")
st.caption("Upload a PDF document to start chatting with its content")

# Show processing summary if available
if st.session_state.document_processed and st.session_state.processing_result:
    with st.expander("Document Processing Summary", expanded=True):
        st.write(f"**Status:** {st.session_state.processing_result['processing_status']}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Images Processed", len(st.session_state.processing_result.get('processed_images', [])))
        col2.metric("Tables Processed", len(st.session_state.processing_result.get('processed_tables', [])))
        col3.metric("Text Chunks Processed", len(st.session_state.processing_result.get('processed_text', [])))
        
        if st.session_state.processing_result.get('storage_status'):
            st.subheader("Storage Results")
            for status in st.session_state.processing_result['storage_status']:
                st.success(status)

# Chat interface
if st.session_state.document_processed:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask a question about the document..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Convert chat history to LangChain messages
            langchain_messages = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))
            
            # Get response from chatbot
            try:
                response = st.session_state.chatbot_agent.invoke({
                    "messages": langchain_messages
                })
                
                # Extract response content
                if hasattr(response, 'content'):
                    full_response = response.content
                elif isinstance(response, dict) and 'messages' in response:
                    full_response = response['messages'][-1].content
                elif isinstance(response, str):
                    full_response = response
                else:
                    full_response = "I couldn't process that request. Please try again."
                    
                # Display response incrementally
                for chunk in full_response.split():
                    full_response_chunk = chunk + " "
                    message_placeholder.markdown(full_response_chunk + "▌")
                    time.sleep(0.05)
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                full_response = f"Error: {str(e)}"
                message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info("Please upload a PDF document to get started")