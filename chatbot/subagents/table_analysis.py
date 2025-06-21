from langgraph.prebuilt import create_react_agent
from chatbot.tools.database_tool import database_query_tool
from chatbot.model import initialize_model

model = initialize_model()

table_analysis_agent = create_react_agent(
    model=model,
    tools=[database_query_tool],
    name="text_analysis_agent",
    prompt="You are a world class table analyser with access to database query tool. As per the query return accurate responses."
)

