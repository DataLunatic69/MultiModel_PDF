from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import Optional
import torch

# Singleton pattern for text vector store
_text_vector_store: Optional[Chroma] = None

def get_text_vector_store() -> Chroma:
    """Get or initialize the persistent text vector store"""
    global _text_vector_store
    if _text_vector_store is None:
        try:
            # Initialize with explicit device mapping
            device = "cuda" if torch.cuda.is_available() else "cpu"
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': device}
            )
            
            _text_vector_store = Chroma(
                collection_name="text_chunks",
                embedding_function=embeddings,
                persist_directory="text_vector_store"
            )
        except Exception as e:
            print(f"❌ Error initializing text vector store: {str(e)}")
            raise
    return _text_vector_store

def get_text_retriever():
    """Get the retriever from the text vector store"""
    return get_text_vector_store().as_retriever()