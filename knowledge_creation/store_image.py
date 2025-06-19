from typing import Dict, Any
import os
import base64
import json
from orchestration.states import DocumentProcessingState

def store_images_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Store images and their descriptions in appropriate storage"""
    
    print("💾 Storing images...")
    
    try:
        
        os.makedirs("./stored_images", exist_ok=True)
        
        
        for i, image_data in enumerate(state["processed_images"]):
            
            image_binary = base64.b64decode(image_data["base64_image"])
            image_filename = f"image_{image_data['index']}_{i}.png"
            image_path = os.path.join("../stored_images", image_filename)
            
            with open(image_path, "wb") as f:
                f.write(image_binary)
            
            
            metadata = {
                "image_path": image_path,
                "caption": image_data["caption"],
                "description": image_data["description"],
                "source_document": image_data["source_document"],
                "processed_at": image_data["processed_at"]
            }
            
            metadata_filename = f"image_metadata_{image_data['index']}_{i}.json"
            metadata_path = os.path.join("../stored_images", metadata_filename)
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
        
        storage_status = f"Images: Successfully stored {len(state['processed_images'])} images"
        
    except Exception as e:
        storage_status = f"Images: Error storing images - {str(e)}"
        print(f"❌ {storage_status}")
    
    print(f"✅ {storage_status}")
    
    return {"storage_status": [storage_status]}