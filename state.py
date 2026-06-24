from typing import List, TypedDict

class GraphState(TypedDict):
    """
    Represents the state of this adaptive RAG Graph.
    """
    
    question:str
    generation:str
    documents: List[str]
    search_count:int
    hallucination_score:str
    relevance_score:str
   