import requests
import pathlib
import time

#######
class SillySolver:

    AUTH = ('ebrown', 'plutonium94')
    PROBLEM_INSTANCE_HASH_ENDPOINT = "https://fluxer.app.sbb.ch/backend/verkehrsplan/calculateHash"
    EMPTY_SOLUTION = "{}"

    @staticmethod
    def solve(problem_instance):
        hash_ = SillySolver._get_problem_instance_hash(problem_instance)
        print(f"Solving {problem_instance} with hash {hash_} \n ...")
        solution = SillySolver._get_canned_sample_solution(problem_instance)
        return (hash_, solution)

    @staticmethod
    def _get_problem_instance_hash(problem_instance):
        problem_instance = {"verkehrsplan": open(problem_instance, 'rb')}
        return requests.post(url=SillySolver.PROBLEM_INSTANCE_HASH_ENDPOINT,
                             files=problem_instance,
                             auth=SillySolver.AUTH,
                             proxies=proxies).json()

    @staticmethod
    def _get_canned_sample_solution(problem_instance):
        print(f"calculating solution for {problem_instance}")
        filename = pathlib.Path(problem_instance).name

        time.sleep(2)
        try:
            canned_solution = pathlib.Path("samples/problem_instances/sample_solutions") / ("solution_" + filename)
            print(f"I have saved the solution to {canned_solution}")
        except:
            print(f"couldn't find solution for {problem_instance}")
            return SillySolver.EMPTY_SOLUTION
        else:
            return canned_solution
#######

# Solving a single problem instance
#######
problem_instance = "samples/problem_instances/01_dummy.json"

mySolver = SillySolver()
mySolver.solve(problem_instance)
#######

# Let's put together a complete solution set
#######
directory = pathlib.Path.cwd()/"samples"/"problem_instances"
problem_instances = directory.glob('*.json')

solution_list = list()

for problem_instance in problem_instances:
    (hash_, sol) = mySolver.solve(problem_instance)
    print("***************************************")
    solution_entry = dict(instance_hash=hash_,
                          solution_path=sol)
    solution_list.append(solution_entry)

from pprint import pprint
pprint(solution_list)
#######

# and submit to grader
#######
def grade_submission(solution_list):
    SOLUTION_VALIDATION_ENDPOINT = "https://fluxer.app.sbb.ch/backend/loesung-validator/validateFile"
    PENALTY_FOR_MISSSING = 1e4
    import csv
    import pandas as pd
    import requests

    # load the list of expected solutions and build lookup dict
    expected_solutions = pd.read_csv("expected_solutions.csv")
    solution_dict = {sol["instance_hash"]: sol["solution_path"] for sol in solution_list}

    # container for collecting the grading results
    grading_results = list()

    # for each expected solution, check if the submission contains one and, if so, have it evaluated
    for hash_ in expected_solutions.problem_instance_hash:
        try:
            solution = solution_dict[hash_]
        except KeyError:
            print(f"No solution submitted for "
                  f"{expected_solutions[expected_solutions.problem_instance_hash == hash_].iat[0,0]}."
                  f"Applying penalty for missing solution")
            grade = dict(problem_instance_hash=hash_,
                         solution_objective=PENALTY_FOR_MISSSING)

        else:  # we have a solution. Send it to the evaluator
            solution_file = {"loesung": solution.open('br')}
            print(f"validating {solution}")
            try:
                time.sleep(1)
                validation_response = requests.post(url=SOLUTION_VALIDATION_ENDPOINT,
                                                files=solution_file,
                                                auth=AUTH,
                                                proxies=proxies,
                                                verify=False)

            except Exception as e:
                print("Error! \n", e)
                grade = dict(problem_instance_hash=hash_,
                             solution_objective=None)

            else:  # validator did send a response
                if validation_response.status_code == 200:
                    grade = dict(problem_instance_hash=hash_,
                                 solution_objective=validation_response.json()["objectiveValue"])
                else:
                    print(f"something went wrong during validation, got response status {validation_response.status_code}")
                    grade = dict(problem_instance_hash=hash_,
                                 solution_objective=None)

        grading_results.append(grade)

    return sum(item["solution_objective"] for item in grading_results if item["solution_objective"] is not None)

#######