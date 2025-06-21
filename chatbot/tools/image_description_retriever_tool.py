# chatbot/tools/image_description_retriever_tool.py
from chatbot.utilise.image_helper import get_image_retriever
from langchain.tools import tool

# Initialize retriever
image_retriever = get_image_retriever()

@tool
def retrieve_image_text(query: str) -> str:
    """
    Retrieve relevant image descriptions based on a query
    
    Args:
        query: The search query string
        
    Returns:
        Concatenated relevant image descriptions or error message
    """
    try:
        docs = image_retriever.get_relevant_documents(query)
        if not docs:
            return "No relevant image descriptions found"
            
        results = []
        for doc in docs:
            results.append(doc.page_content)
            if 'image_path' in doc.metadata:
                results.append(f"Image location: {doc.metadata['image_path']}")
        
        return "\n\n".join(results)
    except Exception as e:
        return f"Image retrieval error: {str(e)}"