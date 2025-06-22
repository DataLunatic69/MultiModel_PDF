from orchestration.workflows import create_document_processing_workflow

def process_document(document_path: str):
    """Process a document through the complete pipeline"""
    
    # Create workflow
    workflow = create_document_processing_workflow()
    
    # Initial state
    initial_state = {
        "document_path": document_path,
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
    
    # Run the workflow
    print("🚀 Starting document processing pipeline...")
    try:
        result = workflow.invoke(initial_state)
        print("\n✨ Document processing completed!")
        return result
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def print_summary(result):
    """Print a nice summary of the processing results"""
    if not result:
        return
    
    print(f"\n🎉 Final Status: {result['processing_status']}")
    
    
    total_images = len(result.get('processed_images', []))
    total_tables = len(result.get('processed_tables', []))
    total_text = len(result.get('processed_text', []))
    
    print(f"\n📊 Processing Summary:")
    print(f"   🖼️  Images processed: {total_images}")
    print(f"   📊 Tables processed: {total_tables}")
    print(f"   📝 Text chunks processed: {total_text}")
    
    
    if result.get('storage_status'):
        print(f"\n💾 Storage Results:")
        for status in result['storage_status']:
            print(f"   ✅ {status}")