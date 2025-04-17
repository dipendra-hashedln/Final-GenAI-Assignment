# app/services/llm_setup.py

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

llm = ChatGroq(
    temperature=0,
    model_name=os.getenv("GROQ_MODEL_NAME", "llama3-8b-8192")
)


