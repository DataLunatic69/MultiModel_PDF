from typing import Dict, Any
from datetime import datetime
from orchestration.states import DocumentProcessingState
from model import initialize_models
from langchain.schema import HumanMessage

def describe_tables_node(state: DocumentProcessingState) -> Dict[str, Any]:
    """Generate descriptions for all extracted tables"""
    
    print("📈 Generating table descriptions...")
    
    model = initialize_models()
    processed_tables = []
    
    for table_data in state["tables"]:
        try:
            prompt = (
                "Analyze the following table and provide a detailed description of its contents, "
                "including the structure, key data points, and any notable trends or insights. "
                f"Here is the table in HTML format: {table_data['table_as_html']} "
                "Directly analyze the table and provide a detailed description without any additional text."
            )
            
            response = model.invoke([HumanMessage(content=prompt)])
            
            processed_tables.append({
                **table_data,
                "description": response.content,
                "processed_at": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"Error processing table {table_data['index']}: {e}")
            processed_tables.append({
                **table_data,
                "description": f"Error generating description: {str(e)}",
                "processed_at": datetime.now().isoformat()
            })
    
    print(f"✅ Generated descriptions for {len(processed_tables)} tables")
    
    return {"processed_tables": processed_tables}