from langgraph.graph import StateGraph, END
from orchestration.states import DocumentProcessingState
from nodes.image_nodes.image_extrator_node import extract_images_node
from nodes.table_nodes.table_extractor_node import extract_tables_node
from nodes.text_nodes.text_extractor_node import extract_text_node
from nodes.image_nodes.describe_image_node import describe_images_node
from nodes.table_nodes.describe_table_node import describe_tables_node  
from nodes.text_nodes.describe_text_node import process_text_node
from nodes.parsing_document_node import parse_document_node
from knowledge_creation.store_image import store_images_node
from knowledge_creation.store_table import store_tables_node
from knowledge_creation.store_text import store_text_node


def create_document_processing_workflow():
    """Create the complete document processing workflow with parallel processing"""
    
    workflow = StateGraph(DocumentProcessingState)
    
    # Add all nodes
    workflow.add_node("parse_document", parse_document_node)
    workflow.add_node("extract_images", extract_images_node)
    workflow.add_node("extract_tables", extract_tables_node)
    workflow.add_node("extract_text", extract_text_node)
    workflow.add_node("describe_images", describe_images_node)
    workflow.add_node("describe_tables", describe_tables_node)
    workflow.add_node("process_text", process_text_node)
    workflow.add_node("store_images", store_images_node)
    workflow.add_node("store_tables", store_tables_node)
    workflow.add_node("store_text", store_text_node)
    
    # Define the workflow exactly as you specified
    workflow.set_entry_point("parse_document")
    
    # Parallel extraction after parsing
    workflow.add_edge("parse_document", "extract_images")
    workflow.add_edge("parse_document", "extract_tables")
    workflow.add_edge("parse_document", "extract_text")
    
    # Description nodes
    workflow.add_edge("extract_images", "describe_images")
    workflow.add_edge("extract_tables", "describe_tables")
    workflow.add_edge("extract_text", "process_text")
    
    # Storage nodes
    workflow.add_edge("describe_images", "store_images")
    workflow.add_edge("describe_tables", "store_tables")
    workflow.add_edge("process_text", "store_text")
    
    # Final consolidation - all end at the same time
    workflow.add_edge("store_images", END)
    workflow.add_edge("store_tables", END)
    workflow.add_edge("store_text", END)
    
    return workflow.compile()