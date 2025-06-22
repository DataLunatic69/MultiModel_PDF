import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stTextInput > div > div > input {
        border-radius: 1rem;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    .stButton > button {
        border-radius: 1rem;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stSpinner {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)