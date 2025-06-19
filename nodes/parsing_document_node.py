from unstructured.partition.pdf import partition_pdf
from typing import Dict, Any
from orchestration.states import DocumentProcessingState


def parse_document_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Parse the PDF document and extract all elements"""
    
    print(f"📄 Parsing document: {state['document_path']}")
    
    try:
       
        raw_chunks = partition_pdf(
            filename=state["document_path"],
            strategy="hi_res",
            infer_table_structure=True,
            extract_image_block_types=["Image", "Figure", "Table"],
            extract_image_block_to_payload=True,
            chunking_strategy=None,
        )
        print(f"✅ Successfully parsed document with {len(raw_chunks)} elements")
        
        text_chunks = partition_pdf(
            filename=state["document_path"],
            strategy="hi_res",
            chunking_strategy="by_title",
            max_characters=2000,
            combine_text_under_n_chars=500,
            new_after_n_chars=1500
        )
        print(f"✅ Successfully chunked text into {len(text_chunks)} chunks")
        
    except Exception as e:
        print(f"❌ Error during document parsing: {e}")
        raw_chunks = []
        text_chunks = []
    
    return {
        "raw_chunks": raw_chunks,
        "text_chunks": text_chunks,
        "processing_status": "parsed"
    }