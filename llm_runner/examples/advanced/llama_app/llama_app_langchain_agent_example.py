import os

from dotenv import load_dotenv

from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import create_agent

# Load environment variables
load_dotenv()

# Load model path from .env
models_dir = os.getenv("MODELS_DIR_PATH")
model_dir = os.getenv("MODEL_DIR_PATH")
model_file_path = os.getenv("MODEL_FILE_PATH")
repo_name = os.getenv("REPO_NAME")

if not models_dir or not model_dir:
    raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

if not model_file_path:
    raise ValueError("Missing MODEL_FILE_PATH in .env")

model_path = os.path.join(models_dir, model_dir, model_file_path)
print(f"Targeting model from .env: {model_path}\n")

# n_gpu_layers = -1 if "NVIDIA" in __import__("torch").__version__ else 0 

# 2. Initialize the LLM within LangChain's ecosystem
llm = ChatLlamaCpp(
    model_path=model_path,
    # temperature=0.7,
    # max_tokens=512,
    # n_ctx=4096,
    # n_gpu_layers=n_gpu_layers, # -1 means offload all layers to GPU if available
    # verbose=False
)

# 3. Define a Tool (e.g., Python REPL or Search)
# def search_tool(query):
#     """Simulated search tool (replace with real duckduckgo/google search)"""
#     return f"Current time is 12:00 PM. The query '{query}' suggests checking local knowledge."

# # 4. Create the Agent
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant."),
#     ("placeholder", "{agent_scratchpad}")
# ])

# from langchain_core.prompts import StringPromptTemplate

# class ToolCallAgent:
#     def __init__(self, llm, tools):
#         self.llm = llm
#         self.tools = tools
        
#     def invoke(self, input_text):
#         # Simple logic to demonstrate interaction
#         response = self.llm.invoke(input_text)
#         return response.content

# agent = ToolCallAgent(llm=llm, tools=[search_tool])

# # 5. Interact
# user_query = "What is the current year? And tell me about Python."
# print(f"User: {user_query}")
# response = agent.invoke(user_query)
# print(f"Model: {response}")


def check_weather(location: str) -> str:
    '''Return the weather forecast for the specified location.'''
    return f"It's always sunny in {location}"

graph = create_agent(
    model=llm,
    tools=[check_weather],
    system_prompt="You are a helpful assistant",
)
inputs = {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
for chunk in graph.stream(inputs, stream_mode="updates"):
    print(chunk)