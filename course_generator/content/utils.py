# content/utils.py

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma"

# Initialize Chroma DB with API key from environment variables
embedding_function = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
