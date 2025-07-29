from langgraph.graph import START, END, StateGraph
from src.LLMs.groqllm import GroqLLM
from src.States.blogstate import BlogState
from src.Nodes.node import Blognode
class Graphbuilder:
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)

    def build_graph(self):
        """Build a graph to generate blogs based on topic"""

        # Nodes
        self.blgnode=Blognode(self.llm)
        self.graph.add_node("Title_generation",self.blgnode.title_creation)
        self.graph.add_node("Content_generation",self.blgnode.content_generator)

        #Edges
        self.graph.add_edge(START,"Title_generation")
        self.graph.add_edge("Title_generation", "Content_generation")
        self.graph.add_edge("Content_generation",END)

        return self.graph
        # self.graph.compile()

    def build_language_graph(self):
        """Build a graph for blog geenration with inputs topic and language"""

        # nodes
        self.blgnode=Blognode(self.llm)
        self.graph.add_node("Title_generation",self.blgnode.title_creation)
        self.graph.add_node("Content_generation",self.blgnode.content_generator)
        self.graph.add_node("Hindi_Translation",lambda state:self.blgnode.translation({**state,"current_language":"hindi"}))
        self.graph.add_node("French_Translation",lambda state:self.blgnode.translation({**state,"current_language":"french"}))
        self.graph.add_node("route",self.blgnode.route)

        # Add Edges
        self.graph.add_edge(START, "Title_generation")
        self.graph.add_edge("Title_generation", "Content_generation")
        self.graph.add_edge("Content_generation","route")
        self.graph.add_conditional_edges("route",
                                         self.blgnode.route_decision,{
                                             "hindi":"Hindi_Translation",
                                             "french":"French_Translation"
                                         })
        self.graph.add_edge("Hindi_Translation",END)
        self.graph.add_edge("French_Translation",END)
        return self.graph


    
    def graph_setup(self, usecase):
        if usecase=="topic":
            self.build_graph()
        if usecase=="language":
            self.build_language_graph()
        return self.graph.compile()
     
# Below code is for the langsmith langgraph studio

llm=GroqLLM().get_llm()

# Get the graph
graphBuilder=Graphbuilder(llm)
graph1=graphBuilder.build_language_graph().compile() # This will be passed in langgraph.json to track in langcsmith


    