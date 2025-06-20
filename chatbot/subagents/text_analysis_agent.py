from langgraph.prebuilt import create_react_agent
from tools.text_retriever_tool import retrieve_text
from ...model import initialize_models

model, _ = initialize_models()

text_analysis_agent = create_react_agent(
    model=model,
    tools=[retrieve_text],
    name="text_analysis_agent",
    prompt="You are a world class text analyser with access to text retreiver to retreive the context. As per the query and the context, return accurate responses."
)

