from typing import Dict, Any
import os
import base64
import json
from orchestration.states import DocumentProcessingState
from chatbot.utilise.image_helper import get_image_vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def store_images_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Store images with robust error handling"""
    logger.info("Starting image storage process")
    storage_status = []
    
    try:
        # Initialize vector store
        try:
            vector_store = get_image_vector_store()
        except Exception as e:
            logger.error(f"Vector store initialization failed: {str(e)}")
            raise
        
        # Create storage directory
        os.makedirs("./stored_images", exist_ok=True)
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=500,
            chunk_overlap=0
        )
        
        texts = []
        metadatas = []

        for i, image_data in enumerate(state["processed_images"]):
            try:
                # Store image file
                image_binary = base64.b64decode(image_data["base64_image"])
                image_filename = f"image_{image_data['index']}_{i}.png"
                image_path = os.path.join("./stored_images", image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_binary)
                
                # Store metadata
                metadata = {
                    "image_path": image_path,
                    "caption": image_data["caption"],
                    "description": image_data["description"],
                    "source_document": image_data["source_document"],
                    "processed_at": image_data["processed_at"]
                }
                
                metadata_filename = f"image_metadata_{image_data['index']}_{i}.json"
                metadata_path = os.path.join("./stored_images", metadata_filename)
                
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f, indent=2)
                
                # Prepare text for vector storage
                combined_text = f"Caption: {image_data['caption']}\nDescription: {image_data['description']}"
                splits = text_splitter.split_text(combined_text)
                
                for split in splits:
                    texts.append(split)
                    metadatas.append({
                        "image_path": image_path,
                        "metadata_path": metadata_path,
                        "source_document": image_data["source_document"],
                        "processed_at": image_data["processed_at"]
                    })
                
            except Exception as e:
                logger.error(f"Error processing image {i}: {str(e)}")
                continue

        # Store in vector database
        if texts:
            try:
                vector_store.add_texts(texts=texts, metadatas=metadatas)
                storage_status.append(f"Images: Stored {len(texts)} description chunks")
                logger.info(f"Successfully stored {len(texts)} text chunks")
            except Exception as e:
                logger.error(f"Failed to store texts: {str(e)}")
                raise
        
        storage_status.append(f"Images: Stored {len(state['processed_images'])} images")
        logger.info("Image storage completed successfully")

    except Exception as e:
        error_msg = f"Images: Storage error - {str(e)}"
        logger.error(error_msg)
        storage_status.append(error_msg)

    return {"storage_status": storage_status}