from urllib import response
from pydantic import BaseModel
import pickle
import requests
from requests.models import Response
import json


class Solver:
    """
    Solver class connects to QpiAI-Opt's cloud server, and run the solver on the passed problem.

    Initialize Solver class with problem and access token

    :type problem: BaseModel
    :param problem: Problem object to be passed from one of the classes in problem directory

    :type url: str
    :param url: Url to access api

    :type access_token: str
    :param access_token: access token to authenticate the solver
    """
    response: Response

    def __init__(self, problem: BaseModel, url: str, access_token: str):
        self.Problem = problem
        self.data = pickle.dumps(problem)
        self.url = url
        self.access_token = access_token
        self.response = None
        self.graph = None
        self.job_id = None
        self.status = "PENDING"

    def run(self, queue=False):
        """
        Runs the problem on the QpiAI-Opt Solver on cloud and receives the response
        """
        if queue:
            response = requests.post(url=f"{self.url}/job/{self.Problem.problem_type}",
                                      headers={"access_token": self.access_token}, data=self.data)
            response = response.json()
            print(response)

            if response["job_id"]:
                self.job_id = response["job_id"]

        else:
            self.response = requests.post(url=f"{self.url}/{self.Problem.problem_type}",
                                      headers={"access_token": self.access_token}, data=self.data)

    def get_result(self):
        """
        to fetch the result after the solver has returned the result of the submitted problem

        :return Response: json
        """
        if self.job_id:
            response = requests.get(url=f"{self.url}/job/{self.job_id}",
                                      headers={"access_token": self.access_token})
            response = response.json()
            print(response)
            if response["status"] == 'SUCCESS':
                self.response = json.loads(response["response"])
                print(self.response)
                result = {'num_nodes': self.response['num_nodes'],
                          'objective': self.response['objective'],
                          'time': self.response['time']}
                return result
            else:
                status = response["status"]
                self.status = status
                print(f"Job Id : {self.job_id} returned with status {status} ")
        else:
            result = {'num_nodes': self.response.json()['num_nodes'],
                    'objective': self.response.json()['objective'],
                    'time': self.response.json()['time']}
            return result

    def get_solution(self):
        if self.response == None:
            print(f"job is {self.status}")
            return
        if isinstance(self.response, dict):
            return self.response.get('solution')
        return self.response.json()['solution']

    def get_qubo_graph(self):
        if self.response:
            try:
                self.graph = self.response.json()['graph']
                return self.response.json()['graph']
            except:
                return self.response
        else:
            print("No response received! Make sure to run the Solver.run() method before accessing response metadata!")
    
    def get_qubo_dict(self):
        self.qubo_dict = dict()
        if self.response:
            try:
                self.graph = self.response.json()['graph']
                if self.graph:
                    l = len(self.graph["weights"])
                    for i in range(l):
                        self.qubo_dict[(self.graph["edges"][0][i], self.graph["edges"][1][i])] = self.graph["weights"][i]
                    return self.qubo_dict
            except:
                # print(e)
                return self.response
        else:
            print("No response received! Make sure to run the Solver.run() method before accessing response metadata!")

