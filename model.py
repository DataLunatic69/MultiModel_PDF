# model.py
from langchain_groq import ChatGroq
import sqlite3
import os

groq_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("MODEL_NAME")

def initialize_models():
    """Initialize the language model and SQL storage system"""
    if not groq_api_key or not model_name:
        raise ValueError("GROQ_API_KEY and MODEL_NAME must be set in environment variables.")
    
    # Initialize model only (remove tuple return)
    model = ChatGroq(
        model_name=model_name,
        groq_api_key=groq_api_key
    )
    
    # Initialize SQL database
    try:
        conn = sqlite3.connect('tables.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS table_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id TEXT UNIQUE,
                description TEXT,
                html_content TEXT,
                source_document TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ SQL database initialized successfully")
    except Exception as e:
        print(f"⚠️ SQL database initialization failed: {e}")
    
    return model  