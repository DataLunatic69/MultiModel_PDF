import glob
from langchain_community.document_loaders import JSONLoader

def load_stored_image_files():
    image_documents = []
    image_files = glob.glob('./stored_images/*.json')
    
    for file_path in image_files:
        try:
            loader = JSONLoader(
                file_path=file_path,
                jq_schema='.',  
                text_content=False
            )
            documents = loader.load()
            image_documents.extend(documents)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return image_documents