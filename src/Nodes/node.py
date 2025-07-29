from src.States.blogstate import BlogState
from langchain_core.messages import HumanMessage, SystemMessage
from src.States.blogstate import Blog
class Blognode:
    """A class to represent blog node"""
    def __init__(self,llm):
        self.llm=llm


    def title_creation(self,state:BlogState):
        """Create the title for the blog"""
        if state['topic'] and "topic" in state:
            prompt="""You are an expert blog content writer, use markdown formatting.
                    Generate blog title for the {topic}. 
                    The title should be creative and SEO friendly."""
            system_message= prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)

            return {"blog":{"title":response.content}}
        
    def content_generator(self, state:BlogState):
        """Generate content based on title"""
        if state["topic"] and "topic" in state:
            prompt="You are an expert blog writter. use Markdown fromatting." \
            "Genrate a detailed blog content with detailed breakdoen for the {topic}"
            system_message=prompt.format(topic=state["topic"])
            response= self.llm.invoke(system_message)
            return{"blog":{"title":state['blog']['title'], "content":response.content}}
        
    def translation(self,state:BlogState):
        """Translate the content to the specified language"""
        translate_prompt="""
                        Translate the following blog into {current_language}.
                        Your response MUST be a JSON object with exactly these two fields:
                        - "title": Translated blog title (as a string)
                        - "content": Translated blog content (as a string)
                        - Maintain the original tone, style and fromatting.
                        - adapt cultural refenrences and idioms to be appropriate for {current_language}

                        Original content:
                        {blog_title}
                        {blog_content}
                    """
        blog_content=state["blog"]["content"]
        blog_title=state["blog"]["title"]
        messages=[
            HumanMessage(translate_prompt.format(current_language=state["current_language"], blog_content=blog_content, blog_title=blog_title))
        ]
        
        # translated_content = self.llm.invoke(translate_prompt).content

        translated_content=self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": {
                    "title":blog_title,
                    "content":translated_content
        }
                }

    def route(self,state:BlogState):
        return {"current_language":state["current_language"]}

    def route_decision(self,state:BlogState):
        """Route the content to the respective translation function"""
        if state["current_language"]=="hindi":
            return "hindi"
        elif state["current_language"]=="french":
            return "french"
        else:
            return state["current_language"]
