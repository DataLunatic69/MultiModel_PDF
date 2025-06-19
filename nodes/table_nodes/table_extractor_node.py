from typing import Dict, Any
from orchestration.states import DocumentProcessingState
from unstructured.documents.elements import Table

def extract_tables_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Extract tables from raw chunks"""
    
    print("📊 Extracting tables...")
    
    table_data = []
    raw_chunks = state["raw_chunks"]
    
    for idx, element in enumerate(raw_chunks):
        if isinstance(element, Table):
            table_data.append({
                "index": idx,
                "table_as_html": element.metadata.text_as_html,
                "table_text": element.text,
                "source_document": state["document_path"]
            })
    
    print(f"✅ Extracted {len(table_data)} tables")
    
    return {"tables": table_data}