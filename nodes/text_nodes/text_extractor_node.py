from typing import Dict, Any
from orchestration.states import DocumentProcessingState
from unstructured.documents.elements import CompositeElement


def extract_text_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Extract and organize text chunks"""
    
    print("📝 Extracting text chunks...")
    
    text_data = []
    text_chunks = state["text_chunks"]
    
    for idx, chunk in enumerate(text_chunks):
        if isinstance(chunk, CompositeElement):
            text_data.append({
                "index": idx,
                "text": chunk.text,
                "element_type": type(chunk).__name__,
                "source_document": state["document_path"]
            })
    
    print(f"✅ Extracted {len(text_data)} text chunks")
    
    return {"text_data": text_data}