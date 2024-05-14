from qiskit.utils import algorithm_globals, QuantumInstance
from qiskit.algorithms import QAOA
from qiskit import BasicAer
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer, CplexOptimizer

class SolveQiskit:
    """
    This class is a wrapper around qiskit's solvers to solve QUBO problems. 
    This class provides two methods to solve the problem, they are
    * qaoa
    * cplex
    
    :type qubo: dict
    :param qubo: qubo represented in a dictionary, for example ``qubo = {(0,0):1, (0,1):-1, (1,0):1, (1,1):-1, (2,0):-3}``.

    :type num_var: int
    :param num_var: number of variables in the qubo.
    """
    def __init__(self, qubo: dict, num_var: int):
        self.qubo = qubo
        self.qp = QuadraticProgram()
        for _ in range(num_var):
            self.qp.binary_var()
        self.qp.minimize(quadratic=self.qubo)
    
    def qaoa(self, quantum_instance: QuantumInstance = QuantumInstance(BasicAer.get_backend("qasm_simulator"))):
        """
        Runs the qiskits MinimumEigenOptmizer to solve the given qubo problem. Can use different backends supported by qiskit.
        
        :type quantum_instance: QuantumInstance
        :param quantum_instance: Can supply the quantum_instance to run on different backends supported by qiskit.

        :return : result containing solution and its objetive
        :rtype : dict
        """
        quantum_instance = quantum_instance
        qaoa_mes = QAOA(quantum_instance=quantum_instance)
        qaoa = MinimumEigenOptimizer(qaoa_mes)
        qaoa_result = qaoa.solve(self.qp)
        return {"solution":[qaoa_result.x], "objective":[qaoa_result.fval]}
    
    def cplex(self):
        """
        Runs CplexOptimizer supported by qiskit which internally runs cplex's solver.

        :return: result
        """
        result = CplexOptimizer().solve(self.qp)
        return result