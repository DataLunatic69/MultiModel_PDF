from loaders.image_description_loader import load_stored_image_files
from utilise.image_helper import create_image_description_vector_store_retriever

image_data = load_stored_image_files()
image_retriever = create_image_description_vector_store_retriever(image_data)

def retrieve_image_text(query):
    """
    Retrieve text chunks based on a query using the vector store retriever.
    
    Args:
        query (str): The query string to search for in the text data.
    
    Returns:
        list: List of retrieved text chunks that match the query.
    """
    response = image_retriever.invoke(query)
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "No relevant text found for the query."