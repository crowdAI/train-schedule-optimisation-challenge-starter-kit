import json
import requests
import pathlib

import pandas as pd
from retry_decorator import retry

class SbbEvaluator:

    AUTH = ('MartyMcFly', 'Uranium-235')
    SCENARIO_UPLOAD_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/uploadVerkehrsplanFile"
    SOLUTION_VALIDATION_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/validateFile"
    PENALTY_FOR_MISSSING_SOLUTION = 1e4


    def __init__(self, answer_file_path, round=1):
        """
        `round` : Holds the round for which the evaluation is being done.
        can be 1, 2...upto the number of rounds the challenge has.
        Different rounds will mostly have different ground truth files.
        """
        self.answer_file_path = answer_file_path
        self.round = round

    def _evaluate(self, client_payload, _context={}):
        """
        `client_payload` will be a dict with (atleast) the following keys :
          - submission_file_path : local file path of the submitted file
        """

        # container for collecting the grading results
        grading_results = list()

        # read in submission
        submission_file_path = client_payload["submission_file_path"]
        submission = pd.read_csv(submission_file_path, skipinitialspace=True)

        # load the list of expected solutions
        expected_solutions = pd.read_csv("evaluator/data/expected_solutions.csv")

        # for each problem instance, check if the submission contains a solution. If so, have it evaluated
        for hash_ in expected_solutions.problem_instance_hash:
            solution = submission[submission.problem_instance_hash == hash_]
            try:
               assert solution.shape == (1, 3)
            except AssertionError:
                print(f"No solution submitted for "
                      f"{expected_solutions[expected_solutions.problem_instance_hash == hash_].iat[0,0]}."
                      f"Applying penalty for missing solution")
                grade = dict(problem_instance_hash=hash_,
                             solution_objective=PENALTY_FOR_MISSSING)

            else:  # we have a solution. Send it to the evaluator
                problem_instance_path = solution.problem_instance_path.iat[0]
                solution_path = solution.solution_path.iat[0]

                upload_status = self._upload_instance(problem_instance_path)

                validation_response = self._evaluate_solution(solution_path)
                print(f"evaluation response: {validation_response.json()}")

                # ToDo: Grade -1 means invalid solution -> also apply PENALTY_FOR_MISSING for this
                grade = dict(problem_instance_hash=hash_,
                             solution_objective=validation_response.json()["objectiveValue"])

            grading_results.append(grade)


        """
        Do something with your submitted file to come up
        with a score and a secondary score.
    
        if you want to report back an error to the user,
        then you can simply do :
          `raise Exception("YOUR-CUSTOM-ERROR")`
    
         You are encouraged to add as many validations as possible
         to provide meaningful feedback to your users
        """
        _result_object = {
            "score": sum(item["solution_objective"] for item in grading_results if item["solution_objective"] is not None),
            "grading_results": grading_results
        }
        return _result_object

    @retry(requests.exceptions.ProxyError, tries=5, delay=10, backoff=2)
    def _evaluate_solution(self, solution_path):
        print(f"trying to grade solution {solution_path}")
        submission_file = {"loesung": self._read_file(solution_path)}
        validation_response = requests.post(self.SOLUTION_VALIDATION_ENDPOINT,
                                            files=submission_file,
                                            auth=self.AUTH)
        print(f"evaluation of solution completed with status code {validation_response.status_code}")
        return validation_response

    @retry(requests.exceptions.ProxyError, tries=5, delay=10, backoff=2)
    def _upload_instance(self, problem_instance_path):
        print(f"trying to upload instance {problem_instance_path}")
        submission_problem_instance_file = {"verkehrsplan": self._read_file(problem_instance_path)}
        upload_response = requests.post(self.SCENARIO_UPLOAD_ENDPOINT,
                                        files=submission_problem_instance_file,
                                        auth=self.AUTH)
        print(f"upload of verkehrsplan completed with status code {upload_response.status_code}")
        return upload_response.status_code

    @staticmethod
    def _read_file(pathname):
        with open(pathname, 'rb') as f:
            return f.read()


if __name__ == "__main__":
    # Lets assume the the ground_truth is a CSV file
    # and is present at data/ground_truth.csv
    # and a sample submission is present at data/sample_submission.csv
    answer_file_path = "data/ground_truth.csv"
    _client_payload = {}
    _client_payload["submission_file_path"] = "evaluator/data/sample_submission.csv"
    # Instaiate a dummy context
    _context = {}
    # Instantiate an evaluator
    crowdai_evaluator = SbbEvaluator(answer_file_path)
    # Evaluate
    result = crowdai_evaluator._evaluate(_client_payload, _context)
    print(result)
