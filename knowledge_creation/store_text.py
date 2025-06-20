from typing import Dict, Any
import os
import json
from orchestration.states import DocumentProcessingState
from model import initialize_models

def store_text_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Store text chunks in both vector database and as local JSON"""
    
    print("🔍 Storing text in vector database and local JSON...")

    try:
        _, vector_store = initialize_models()

        # Always create ./stored_text and store as JSON
        os.makedirs("./stored_text", exist_ok=True)

        for i, text_data in enumerate(state["processed_text"]):
            text_filename = f"text_chunk_{text_data['index']}_{i}.json"
            text_path = os.path.join("./stored_text", text_filename)
            with open(text_path, "w") as f:
                json.dump(text_data, f, indent=2)

        json_storage_msg = f"Text: Stored {len(state['processed_text'])} text chunks as JSON files"

        # Also store in vector DB if available
        if vector_store is not None:
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

            vector_store.add_texts(texts=texts, metadatas=metadatas)
            vector_storage_msg = f"Text: Successfully stored {len(texts)} text chunks in vector database"
        else:
            vector_storage_msg = "Text: Vector store not available, skipped vector storage."

        storage_status = [json_storage_msg, vector_storage_msg]

    except Exception as e:
        error_msg = f"Text: Error storing text - {str(e)}"
        print(f"❌ {error_msg}")
        storage_status = [error_msg]

    for msg in storage_status:
        print(f"✅ {msg}")

    return {"storage_status": storage_status}
