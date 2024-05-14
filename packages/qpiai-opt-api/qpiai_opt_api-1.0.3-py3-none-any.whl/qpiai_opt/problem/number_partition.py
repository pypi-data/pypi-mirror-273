from pydantic import BaseModel
from typing import Optional

class NumberPartitionProblem(BaseModel):
    '''class representing a Number Partition problem to feed the inputs to the solver
    :type length: int
    :param length: Length of the list of the numbers to be partitioned equally

    :type numbers: Optional[list]
    :param numbers: List of numbers to be partitioned. If not passed as an input, the problem class generates a random list of size length

    :type penalty: int
    :param penalty: penalty term used in the QUBO formulation.

    :type max_evaluations: int
    :param max_evaluations: Number of maximum evaluations to be run to search the solution.
        '''
    class Config:
        arbitrary_types_allowed = True

    length: int = 100
    numbers: Optional[list] = None
    penalty: int = 2
    max_evaluations: int = 1000
    problem_type: str = "numberPartition"
