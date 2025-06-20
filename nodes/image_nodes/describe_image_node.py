from typing import Dict, Any
from datetime import datetime
from orchestration.states import DocumentProcessingState
from model import initialize_models
from langchain.schema import HumanMessage

def describe_images_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Generate descriptions for all extracted images"""
    
    print("🔍 Generating image descriptions...")
    
    model = initialize_models()
    processed_images = []
    
    for image_data in state["images"]:
        try:
            prompt = (
                f"Describe the image in detail. The caption is: {image_data['caption']}. "
                f"The image text is: {image_data['image_text']} "
                f"Directly analyze the image and provide a detailed description without any additional text."
            )
            
            response = model.invoke([HumanMessage(content=prompt)])
            
            processed_images.append({
                **image_data,
                "description": response.content,
                "processed_at": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"Error processing image {image_data['index']}: {e}")
            processed_images.append({
                **image_data,
                "description": f"Error generating description: {str(e)}",
                "processed_at": datetime.now().isoformat()
            })
    
    print(f"✅ Generated descriptions for {len(processed_images)} images")
    
    return {"processed_images": processed_images}