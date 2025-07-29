import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self):
        load_dotenv()

    def get_llm(self):
        try:
            os.environ['GROQ_API_KEY']=self.groq_api_key=os.getenv("GROQ_API_KEY")
            llm=ChatGroq(model="llama-3.1-8b-instant", api_key=self.groq_api_key)
            return llm
        except Exception as e:
            raise ValueError(f"Error occur due to: {e}")