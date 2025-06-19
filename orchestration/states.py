from typing import TypedDict, List, Dict, Any
from typing_extensions import Annotated
from operator import add


class DocumentProcessingState(TypedDict):
    document_path: str
    raw_chunks: List[Any]
    text_chunks: List[Any]
    
    images: Annotated[List[Dict[str, Any]], add]
    tables: Annotated[List[Dict[str, Any]], add] 
    text_data: Annotated[List[Dict[str, Any]], add]
    
  
    processed_images: Annotated[List[Dict[str, Any]], add]
    processed_tables: Annotated[List[Dict[str, Any]], add]
    processed_text: Annotated[List[Dict[str, Any]], add]
    
   
    storage_status: Annotated[List[str], add]
    

    processing_status: str