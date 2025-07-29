from pydantic import BaseModel, Field
from typing import TypedDict

class Blog(BaseModel):
    title:str=Field(description="Title of the blog post")
    content:str=Field(description="The main content of the blog")

class BlogState(TypedDict):
    topic:str
    blog:Blog
    current_language:str
