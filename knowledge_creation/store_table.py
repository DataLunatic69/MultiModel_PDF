from typing import Dict, Any
import sqlite3
from orchestration.states import DocumentProcessingState

def store_tables_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Store tables in SQL database"""
    
    print("🗄️ Storing tables in SQL database...")
    
    try:
        conn = sqlite3.connect('tables.db')
        cursor = conn.cursor()
        
        for table_data in state["processed_tables"]:
            table_id = f"table_{table_data['index']}_{hash(table_data['source_document'])}"
            
            # Insert or update table metadata
            cursor.execute('''
                INSERT OR REPLACE INTO table_metadata 
                (table_id, description, html_content, source_document)
                VALUES (?, ?, ?, ?)
            ''', (
                table_id,
                table_data["description"],
                table_data["table_as_html"],
                table_data["source_document"]
            ))
        
        conn.commit()
        conn.close()
        
        storage_status = f"Tables: Successfully stored {len(state['processed_tables'])} tables in SQL database"
        
    except Exception as e:
        storage_status = f"Tables: Error storing tables - {str(e)}"
        print(f"❌ {storage_status}")
    
    print(f"✅ {storage_status}")
    
    return {"storage_status": [storage_status]}
