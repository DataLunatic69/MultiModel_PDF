# chatbot/tools/text_retriever_tool.py
from chatbot.utilise.text_helper import get_text_retriever
from langchain.tools import tool

# Initialize retriever
text_retriever = get_text_retriever()

@tool
def retrieve_text(query: str) -> str:
    """
    Retrieve relevant text chunks based on a query
    
    Args:
        query: The search query string
        
    Returns:
        Concatenated relevant text chunks with metadata
    """
    try:
        docs = text_retriever.invoke(query)
        if not docs:
            return "No relevant text found"
            
        results = []
        for doc in docs:
            results.append(doc.page_content)
            if 'json_path' in doc.metadata:
                results.append(f"Source: {doc.metadata['source_document']}")
                results.append(f"Full text available at: {doc.metadata['json_path']}")
        
        return "\n\n".join(results)
    except Exception as e:
        return f"Text retrieval error: {str(e)}"