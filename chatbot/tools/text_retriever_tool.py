from chatbot.loaders.text_loader import load_stored_text_files
from chatbot.utilise.text_helper import create_vector_store_retriever
from langchain.tools import tool

text_data = load_stored_text_files()
retriever= create_vector_store_retriever(text_data)

@tool
def retrieve_text(query):
    """
    Retrieve text chunks based on a query using the vector store retriever.
    
    Args:
        query (str): The query string to search for in the text data.
    
    Returns:
        list: List of retrieved text chunks that match the query.
    """
    response = retriever.invoke(query)
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "No relevant text found for the query."