from typing import Dict, Any
from orchestration.states import DocumentProcessingState
from unstructured.documents.elements import FigureCaption
from unstructured.documents.elements import Image

def extract_images_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Extract images and their captions from raw chunks"""
    
    print("🖼️ Extracting images...")
    
    all_images = []
    raw_chunks = state["raw_chunks"]
    
    for idx, chunk in enumerate(raw_chunks):
        if isinstance(chunk, Image):
            # Check if next chunk is a figure caption
            caption = None
            if idx + 1 < len(raw_chunks) and isinstance(raw_chunks[idx + 1], FigureCaption):
                caption = raw_chunks[idx + 1].text
            
            all_images.append({
                "index": idx,
                "caption": caption if caption else "No caption",
                "image_text": chunk.text,
                "base64_image": chunk.metadata.image_base64,
                "source_document": state["document_path"]
            })
    
    print(f"✅ Extracted {len(all_images)} images")
    
    return {"images": all_images}