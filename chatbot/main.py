# chatbot/main.py
import os
from langchain.schema import HumanMessage

from chatbot.model import initialize_model
from chatbot.subagents.image_analysis_agent import image_text_analysis_agent
from chatbot.subagents.text_analysis_agent import text_analysis_agent
from langgraph_supervisor import create_supervisor

def create_supervisor_app():
    """Create and compile the supervisor workflow"""
    # Initialize core components
    print("🚀 Initializing model...")
    model = initialize_model()
   
    # Define supervisor with agents
    print("🧠 Creating supervisor workflow...")  
    supervisor_workflow = create_supervisor(
        agents=[text_analysis_agent, image_text_analysis_agent],
        model=model,
        prompt=(
            "You are a supervisor managing multiple agents. "
            "Use the appropriate agent based on the input type (text or image)."
        ),
        output_mode="last_message",
        supervisor_name="supervisor_agent",
    )

    return supervisor_workflow.compile()

# CLI entry point remains for testing
if __name__ == "__main__":
    supervisor_app = create_supervisor_app()

    # Sample query
    print("💬 Running sample query...")
    response = supervisor_app.invoke({
        "messages": [HumanMessage(content="what is query decomposition?")]
    })

    print("\n📨 Response:")
    print(response)