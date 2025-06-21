# streamlit_app/utils.py
import streamlit as st

def display_processing_summary(result):
    """Display processing summary in Streamlit"""
    if not result:
        return
    
    st.subheader("Processing Summary")
    st.write(f"**Status:** {result['processing_status']}")
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Images Processed", len(result.get('processed_images', [])))
    col2.metric("Tables Processed", len(result.get('processed_tables', [])))
    col3.metric("Text Chunks Processed", len(result.get('processed_text', [])))
    
    # Show storage status
    if result.get('storage_status'):
        st.subheader("Storage Results")
        for status in result['storage_status']:
            st.success(status)