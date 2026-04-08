import os
from typing import List

from dotenv import load_dotenv
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain.messages import AIMessage
from langchain.tools import tool

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


@tool
def validate_user(user_id: int, addresses: List[str]) -> bool:
    """Validate user using historical addresses.

    Args:
        user_id (int): the user ID.
        addresses (List[str]): Previous addresses as a list of strings.
    """
    return True


llm = ChatLlamaCpp(
    model_path=model_path,
    validate_model_on_init=True,
    temperature=0,
    verbose=False,
).bind_tools([validate_user])

result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)

print(result)

if isinstance(result, AIMessage) and result.tool_calls:
    print(result.tool_calls)
