from langchain_groq import ChatGroq
import sqlite3
from langchain_community.vectorstores import Chroma
import os

groq_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("MODEL_NAME")

def initialize_models():
    """Initialize the language model and storage systems"""
    model = ChatGroq(
        model_name=model_name, 
        groq_api_key=groq_api_key
    )
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vector_store = Chroma(
            collection_name="document_text",
            embedding_function=embeddings,
            persist_directory="./vectorstore_db"
        )
        print("✅ Vector store initialized successfully")
        
    except Exception as e:
        print(f"⚠️ Vector store initialization failed: {e}")
        print("📝 Will continue without vector storage...")
        vector_store = None
    

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
    
    return model, vector_store