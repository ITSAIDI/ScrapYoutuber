from langgraph.graph import END, StateGraph, START
from The_State import State
from  Functions import Create_RAG,Get_Context,Extractor_function,Generator_function,Condition,Web



graph_builder = StateGraph(State)

graph_builder.add_node("Fetch",Create_RAG)
graph_builder.add_node("RAG",Get_Context)
graph_builder.add_node("Extractor",Extractor_function)
graph_builder.add_node("Generator",Generator_function)
graph_builder.add_node("Web",Web)

graph_builder.add_edge(START, "Fetch")
graph_builder.add_edge("Fetch", "Generator")
graph_builder.add_edge("Generator","Web")
graph_builder.add_edge("Web","RAG")
graph_builder.add_edge("RAG","Extractor")
graph_builder.add_conditional_edges("Extractor",Condition,{"END":"__end__","CONTINUE":"Generator"})
Graph = graph_builder.compile()











