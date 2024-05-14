import dimod
import neal
class SolveDwave:
    """
    This class is a wrapper around dwave's solvers to solve QUBO problems. 
    This class provides four methods to solve the problem, they are
    * exact_solver
    * simulated_annealing_sampler
    * neal_simulated_annealer
    * random_sampler
    
    :type qubo: dict
    :param qubo: qubo represented in a dictionary, for example ``qubo = {(0,0):1, (0,1):-1, (1,0):1, (1,1):-1, (2,0):-3}``
    """
    def __init__(self, qubo: dict):
        self.qubo = qubo
    
    def exact_solver(self):
        """
        Returns the exact solution for the qubo. Not suitable for bigger problems as it does an exhaustive search ibn the solution space.
        :return sampled set of solutions
        """
        return dimod.ExactSolver().sample_qubo(self.qubo)
    
    def simulated_annealing_sampler(self):
        """
        This simulated annealing solver implements a straightforward approach of the simulated annealer(Only for testing and debugging locally). Not suitable for bigger problems as it is not the best implementation, instead use ``neal_simulated_annealer`` for larger problems.
        :return sampled set of solutions
        """
        return dimod.SimulatedAnnealingSampler().sample_qubo(self.qubo)
    
    def neal_simulated_annealer(self):
        """
        This is a high performant implementation of simulated annealer given by Dwave-neal.
        :return sampled set of solutions
        """
        return neal.SimulatedAnnealingSampler().sample_qubo(self.qubo)
    
    def random_sampler(self):
        """
        This methhod performs a random sampling of the solutions and returns the sample set.
        :return sampled set of solutions
        """
        return dimod.RandomSampler().sample_qubo(self.qubo)
