from typing import Dict, Any
import os
import json
from orchestration.states import DocumentProcessingState
from chatbot.utilise.text_helper import get_text_vector_store
import torch

def store_text_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Store text chunks in vector database and as local JSON"""
    print("🔍 Storing text in vector database and local JSON...")
    storage_status = []
    
    try:
        # Initialize vector store with error handling
        try:
            vector_store = get_text_vector_store()
        except Exception as e:
            raise Exception(f"Failed to initialize vector store: {str(e)}")

        # Create storage directory
        os.makedirs("./stored_text", exist_ok=True)
        texts = []
        metadatas = []

        for i, text_data in enumerate(state["processed_text"]):
            # Store as JSON file
            text_filename = f"text_chunk_{text_data['index']}_{i}.json"
            text_path = os.path.join("./stored_text", text_filename)
            with open(text_path, "w") as f:
                json.dump(text_data, f, indent=2)
            
            # Prepare for vector storage
            texts.append(text_data["text"])
            metadatas.append({
                "index": text_data["index"],
                "element_type": text_data["element_type"],
                "source_document": text_data["source_document"],
                "word_count": text_data["word_count"],
                "char_count": text_data["char_count"],
                "processed_at": text_data["processed_at"],
                "json_path": text_path
            })

        # Store in vector database with device awareness
        if texts:
            try:
                with torch.no_grad():  # Disable gradient calculation
                    vector_store.add_texts(texts=texts, metadatas=metadatas)
                storage_status.append(f"Text: Stored {len(texts)} chunks in vector database")
            except Exception as e:
                raise Exception(f"Failed to add texts to vector store: {str(e)}")
        
        storage_status.append(f"Text: Stored {len(texts)} text chunks as JSON files")

    except Exception as e:
        error_msg = f"Text: Error storing text - {str(e)}"
        print(f"❌ {error_msg}")
        storage_status.append(error_msg)

    for msg in storage_status:
        if "Error" not in msg:
            print(f"✅ {msg}")

    return {"storage_status": storage_status}