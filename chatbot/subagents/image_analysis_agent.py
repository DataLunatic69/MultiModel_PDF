from langgraph.prebuilt import create_react_agent
from tools.image_description_retriever_tool  import retrieve_image_text
from model import initialize_models

model, _ = initialize_models()

image_text_analysis_agent = create_react_agent(
    model=model,
    tools=[retrieve_image_text],
    name="image_text_analysis_agent",
    prompt="You are a world class text analyser with access to image text retreiver to retreive the context from the available description of various images. As per the query and the context, return accurate responses."
)

