from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import Optional
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable declaration
_image_vector_store: Optional[Chroma] = None

def get_image_vector_store() -> Chroma:
    """Initialize image vector store with proper device handling"""
    global _image_vector_store
    
    if _image_vector_store is None:
        try:
            # Force CPU initialization first
            logger.info("Initializing embeddings with CPU first")
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Test embeddings
            test_embedding = embeddings.embed_query("test")
            logger.info(f"Embedding test successful. Vector length: {len(test_embedding)}")
            
            # Now try GPU if available
            if torch.cuda.is_available():
                try:
                    logger.info("Attempting GPU initialization")
                    embeddings = HuggingFaceEmbeddings(
                        model_name="all-MiniLM-L6-v2",
                        model_kwargs={'device': 'cuda'},
                        encode_kwargs={'normalize_embeddings': True}
                    )
                    test_embedding = embeddings.embed_query("test")
                    logger.info("GPU initialization successful")
                except Exception as e:
                    logger.warning(f"GPU initialization failed, falling back to CPU: {str(e)}")
            
            _image_vector_store = Chroma(
                collection_name="image_descriptions",
                embedding_function=embeddings,
                persist_directory="image_vector_store"
            )
            logger.info("Image vector store initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize image vector store: {str(e)}")
            raise RuntimeError(f"Image vector store initialization failed: {str(e)}")
    
    return _image_vector_store

def get_image_retriever():
    """Get the retriever from the image vector store"""
    return get_image_vector_store().as_retriever()