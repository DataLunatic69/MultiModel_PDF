from langgraph_supervisor import create_supervisor
from subagents.image_analysis_agent import image_text_analysis_agent
from subagents.text_analysis_agent import text_analysis_agent
from langchain.schema import HumanMessage
from model import initialize_models

model, _ = initialize_models()

supervisor_workflow = create_supervisor(
    agents=[text_analysis_agent, image_text_analysis_agent],
    model=model,
    prompt=(
        "You are a supervisor managing a weather agent. "
        "For any weather-related question, call the 'weather_agent' to handle it."
    ),
    output_mode="last_message",
    #output_mode="full_history",
    supervisor_name="supervisor_agent",
)

supervisor_app = supervisor_workflow.compile()

supervisor_app.invoke(
    {"messages": [HumanMessage(content="what is query decomposition?")]}
)