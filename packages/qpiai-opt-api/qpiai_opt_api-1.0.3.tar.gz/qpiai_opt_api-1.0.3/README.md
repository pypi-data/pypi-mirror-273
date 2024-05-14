# qpiai-opt-api

qpiai-opt-api provides a python package to interface with the qpiai-opt solver on the cloud to solve NP-Hard Combinatorial problems.

QpiAI-Opt is a high-level optimization library to solve NP-Hard (combinatorial) problems. We provide access to our solvers through QpiAI-Opt API to access four base class problems (that have real-world applications):
1) Maximum Cut

2) Minimum Vertex Cover

3) Maximum Independent Set

4) Number Partition


QpiAI-Opt API also provides a **QUBO design engine** to express a general QUBO problem and solve it with our solver.

# Installation steps

1. Install the latest version of the project from: https://pypi.org/project/qpiai-opt-api/1.0.1/
You can use the following command to install.
    
    `pip install qpiai-opt-api==1.0.1`

2. Install the dependencies from requirements.txt

    `pip install networkx`

    `pip install requests`

    

3. You are ready to access the solvers using the url and access token. Refer to the below tutorial to get started.

4. In order to use the wrappers for dwave and qiskit support, install the following dependencies.
    `pip install qiskit`

    `pip install qiskit[optimization]`

    `pip install 'qiskit-optimization[cplex]`

    `pip install dimod`

    `pip install dwave-neal`

# What's new?

We have added dwave and qiskit wrappers to solve the qubo problem on both the platforms, besides qpiai_opt's solver. Refer to documentaion for more info.

You can also refer to the below turorials to get started with qpiai_opt and its wrappers to solve on supported platforms.

# Tutorials

Refer to [QpiAI-API tutorials](https://gitlab.qpiai.tech/qpiquantum/optimisation/qpiai-opt-api/-/tree/main/tutorials)



