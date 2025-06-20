import glob
from langchain_community.document_loaders import JSONLoader

def load_stored_text_files():
    text_documents = []
    text_files = glob.glob('./stored_text/*.json')
    
    for file_path in text_files:
        try:
            loader = JSONLoader(
                file_path=file_path,
                jq_schema='.', 
                text_content=False
            )
            documents = loader.load()
            text_documents.extend(documents)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return text_documents