from typing import Union
import networkx as nx
from pydantic import BaseModel
from typing import Optional

class MaximumCutProblem(BaseModel):
    '''class representing a Maximum-Cut problem to feed the inputs to the solver

    Objective function:

    :type num_nodes: int
    :param num_nodes: Number of nodes in the problem graph

    :type graph: Optional[Union[dict, networkx.Graph]]
    :param graph: Graph to be solved for maximum cut. If the graph is not passed the problem method generates a random graph as per given num_nodes.

    :type penalty: int
    :param penalty: penalty term used in the QUBO formulation.

    :type max_evaluations: int
    :param max_evaluations: Number of maximum evaluations to be run to search the solution.

    :type load_gset: Optional[str]
    :param load_gset: Specify one among the G1,...,G77 Stanford Gset dataset or keep it none to pass a graph
    or generate a graph.
    '''
    class Config:
        arbitrary_types_allowed = True

    num_nodes: int = 100
    graph: Optional[Union[dict, nx.Graph]] = None
    penalty: int = 2
    max_evaluations: int = 1000
    load_gset: Optional[str] = None
    problem_type: str = "maximumCut"
