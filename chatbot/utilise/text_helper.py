from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

def create_vector_store_retriever(text_data, persist_directory="text_vector_store", chunk_size=500, chunk_overlap=0):
    """
    Creates a vector store and retriever from text documents.
    
    Args:
        text_data: List of loaded text documents
        persist_directory: Directory to persist the vector store (default: "text_vector_store")
        chunk_size: Size of text chunks for splitting (default: 500)
        chunk_overlap: Overlap between chunks (default: 0)
    
    Returns:
        tuple: (vector_store, retriever, vector_store_index)
    """

    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    doc_splits = text_splitter.split_documents(text_data)
    
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create vector store
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory,  
    )
    
    # Add documents to vector store
    vector_store.add_documents(doc_splits)
    print(f"Inserted {len(doc_splits)} documents.")
    
    # Create index wrapper and retriever
    vector_store_index = VectorStoreIndexWrapper(vectorstore=vector_store)
    retriever = vector_store.as_retriever()
    
    return  retriever