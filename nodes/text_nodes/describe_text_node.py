from typing import Dict, Any
from datetime import datetime
from orchestration.states import DocumentProcessingState

def process_text_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Process text chunks and add metadata"""
    
    print("⚡ Processing text chunks...")
    
    processed_text = []
    
    for text_data in state["text_data"]:
        processed_text.append({
            **text_data,
            "word_count": len(text_data["text"].split()),
            "char_count": len(text_data["text"]),
            "processed_at": datetime.now().isoformat()
        })
    
    print(f"✅ Processed {len(processed_text)} text chunks")
    
    return {"processed_text": processed_text}