# document_processor/processor.py
import os
import json
from typing import Dict, Any
from orchestration.workflows import create_document_processing_workflow

class DocumentProcessor:
    def __init__(self):
        self.processing_result = None
        self.processing_complete = False
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process document and store results"""
        workflow = create_document_processing_workflow()
        
        initial_state = {
            "document_path": file_path,
            "raw_chunks": [],
            "text_chunks": [],
            "images": [],
            "tables": [],
            "text_data": [],
            "processed_images": [],
            "processed_tables": [],
            "processed_text": [],
            "storage_status": [],
            "processing_status": "initialized"
        }
        
        result = workflow.invoke(initial_state)
        self._save_processing_result(result)
        self.processing_complete = True
        return result
    
    def _save_processing_result(self, result: Dict[str, Any]):
        """Save processing results to disk"""
        os.makedirs("processing_results", exist_ok=True)
        with open("processing_results/latest.json", "w") as f:
            json.dump(result, f)
    
    def load_processing_result(self) -> bool:
        """Load previous processing results"""
        try:
            with open("processing_results/latest.json", "r") as f:
                self.processing_result = json.load(f)
            self.processing_complete = True
            return True
        except:
            return False

processor = DocumentProcessor()