from typing import Union
import networkx as nx
from pydantic import BaseModel


class QUBOProblem(BaseModel):
    '''class representing a Maximum Independent Set problem to feed the inputs to the solver
    :type num_variables: int
    :param num_variables: Number of variables in the QUBO

    :type qubo_dict: Optional[dict]
    :param qubo_dict: QUBO to be passed in the form of a dictionary. Every key is an edge represented by tuples of node numbers, and every value is the weight of that edge.

    :type max_evaluations: int
    :param max_evaluations: Number of maximum evaluations to be run to search the solution.
    '''
    class Config:
        arbitrary_types_allowed = True
    num_variables: int = 100
    qubo_dict: dict = None
    max_evaluations: int = 1000
    problem_type: str = "QUBO"