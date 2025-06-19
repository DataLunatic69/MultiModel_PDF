from typing import Dict, Any
import os
import json
from orchestration.states import DocumentProcessingState
from model import initialize_models

def store_text_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Store text chunks in vector database"""
    
    print("🔍 Storing text in vector database...")
    
    try:
        _, vector_store = initialize_models()
        
        if vector_store is None:
            # Fallback: store as JSON files
            os.makedirs("../stored_text", exist_ok=True)
            
            for i, text_data in enumerate(state["processed_text"]):
                text_filename = f"text_chunk_{text_data['index']}_{i}.json"
                text_path = os.path.join("../stored_text", text_filename)
                
                with open(text_path, "w") as f:
                    json.dump(text_data, f, indent=2)
            
            storage_status = f"Text: Stored {len(state['processed_text'])} text chunks as JSON files (vector store unavailable)"
        else:
            # Prepare documents for vector storage
            texts = []
            metadatas = []
            
            for text_data in state["processed_text"]:
                texts.append(text_data["text"])
                metadatas.append({
                    "index": text_data["index"],
                    "element_type": text_data["element_type"],
                    "source_document": text_data["source_document"],
                    "word_count": text_data["word_count"],
                    "char_count": text_data["char_count"],
                    "processed_at": text_data["processed_at"]
                })
            
            # Add to vector store
            vector_store.add_texts(texts=texts, metadatas=metadatas)
            
            storage_status = f"Text: Successfully stored {len(texts)} text chunks in vector database"
        
    except Exception as e:
        storage_status = f"Text: Error storing text - {str(e)}"
        print(f"❌ {storage_status}")
    
    print(f"✅ {storage_status}")
    
    return {"storage_status": [storage_status]}