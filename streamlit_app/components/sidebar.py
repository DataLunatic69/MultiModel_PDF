import streamlit as st
import sqlite3
from chatbot.utilise.text_helper import get_text_retriever
from chatbot.utilise.image_helper import get_image_retriever

def show_sidebar_content():
    """Display all sidebar components"""
    show_system_status()
    st.markdown("<hr>", unsafe_allow_html=True)
    show_usage_tips()

def show_system_status():
    """Display system status information"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1rem; border-radius: 1rem; margin-bottom: 1rem;">
        <h3 style="margin: 0; text-align: center;">🔧 System Status</h3>
    </div>
    """, unsafe_allow_html=True)
    
    check_text_retrieval()
    check_image_retrieval()
    check_table_database()

def check_text_retrieval():
    """Check text retrieval system status"""
    try:
        text_retriever = get_text_retriever()
        test_docs = text_retriever.get_relevant_documents("test", k=1)
        show_status_item(
            "Text Retrieval",
            "✅ Online",
            f"Documents: {len(test_docs) if test_docs else 0}",
            "#28a745"
        )
    except Exception as e:
        show_status_item(
            "Text Retrieval", 
            "❌ Error",
            str(e)[:50] + "..." if len(str(e)) > 50 else str(e),
            "#dc3545"
        )

def check_image_retrieval():
    """Check image retrieval system status"""
    try:
        image_retriever = get_image_retriever()
        test_docs = image_retriever.get_relevant_documents("test", k=1)
        show_status_item(
            "Image Analysis",
            "✅ Online",
            f"Images: {len(test_docs) if test_docs else 0}",
            "#28a745"
        )
    except Exception as e:
        show_status_item(
            "Image Analysis",
            "❌ Error", 
            str(e)[:50] + "..." if len(str(e)) > 50 else str(e),
            "#dc3545"
        )

def check_table_database():
    """Check table database status"""
    try:
        conn = sqlite3.connect('tables.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM table_metadata")
        count = cursor.fetchone()[0]
        conn.close()
        show_status_item(
            "Table Database",
            "✅ Online",
            f"Tables: {count}",
            "#28a745"
        )
    except Exception as e:
        show_status_item(
            "Table Database",
            "❌ Error",
            str(e)[:50] + "..." if len(str(e)) > 50 else str(e),
            "#dc3545"
        )

def show_status_item(name: str, status: str, details: str, color: str):
    """Display a status item with consistent styling"""
    st.markdown(f"""
    <div style="background: white; border-left: 4px solid {color}; 
                padding: 0.75rem; margin: 0.5rem 0; border-radius: 0.5rem; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <strong style="color: #333;">{name}</strong><br>
        <span style="color: {color};">{status}</span><br>
        <small style="color: #666;">{details}</small>
    </div>
    """, unsafe_allow_html=True)

def show_usage_tips():
    """Display usage tips for better user experience"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                color: white; padding: 1rem; border-radius: 1rem; margin: 1rem 0;">
        <h3 style="margin: 0 0 0.5rem 0;">💡 Usage Tips</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tips = [
        "📝 Ask about text content: concepts, definitions, explanations",
        "🖼️ Query image descriptions and visual content", 
        "📊 Analyze tables and data relationships",
        "🔍 Request specific details or summaries",
        "❓ Try follow-up questions for deeper insights"
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div style="background: white; padding: 0.5rem; margin: 0.25rem 0; 
                    border-radius: 0.5rem; border-left: 3px solid #f5576c;">
            <small style="color: #333;">{tip}</small>
        </div>
        """, unsafe_allow_html=True)