import uvicorn
from fastapi import FastAPI, Request
from src.Graphs.graphbuilder import Graphbuilder
from src.LLMs.groqllm import GroqLLM
import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

app=FastAPI()
os.environ["langsmith_api_key"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

# APIs

@app.post("/blogs")
async def create_blogs(request:Request):
    data=await request.json()
    topic=data.get("topic","") # returns "" if topic is missing 
    current_language=data.get("language","")

    #get llm object
    llm=GroqLLM()
    llm=llm.get_llm()

    #get the Graph
    workflow=Graphbuilder(llm)
    if current_language and topic:
        graph=workflow.graph_setup(usecase="language")
        state=graph.invoke({"topic":topic, "current_language":current_language})
    elif topic:
        graph=workflow.graph_setup(usecase="topic")
        state=graph.invoke({"topic":topic})
    

    return {"data":state}


if __name__=="__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
