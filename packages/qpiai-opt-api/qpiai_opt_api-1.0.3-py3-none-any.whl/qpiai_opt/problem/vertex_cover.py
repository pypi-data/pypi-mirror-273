from typing import Union, Optional
import networkx as nx
from pydantic import BaseModel

class MinimumVertexCoverProblem(BaseModel):
    """class representing a Minimum Vertex Cover problem to feed the inputs to the solver
    :type num_nodes: int
    :param num_nodes: Number of nodes in the problem graph

    :type graph: Optional[Union[dict, networkx.Graph]]
    :param graph: Graph to be solved for maximum cut. If the graph is not passed the problem method generates a random graph as per given num_nodes.

    :type penalty: int
    :param penalty: penalty term used in the QUBO formulation.

    :type max_evaluations: int
    :param max_evaluations: Number of maximum evaluations to be run to search the solution.
        """
    class Config:
        arbitrary_types_allowed = True
    num_nodes: int = 100
    graph: Optional[Union[dict, nx.Graph]] = None
    penalty: int = 2
    max_evaluations: int = 1000
    problem_type: str = "minimumVertexCover"