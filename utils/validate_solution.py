import requests

AUTH = ('MartyMcFly', 'Uranium-235')
SCENARIO_UPLOAD_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/uploadVerkehrsplanFile"
SOLUTION_VALIDATION_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/validateFile"

scenario = "sample_files/sample_scenario_simple.json"
solution = "sample_files/sample_scenario_simple_solution.json"


def do_loesung_validation(scenario, solution):

    # upload scenario first (may not be available in the store)
    scenario_file = {"verkehrsplan": open(scenario, 'rb')}
    upload_response = requests.post(SCENARIO_UPLOAD_ENDPOINT, files=scenario_file, auth=AUTH, proxies=proxies)
    print(f"upload finished with status {upload_response}")

    # now we can validate
    solution_file = {"loesung": open(solution, 'rb')}
    validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH, proxies=proxies)
    print(f"validation finished with status {validation_response}")
    return validation_response.json()

validation_result = do_loesung_validation(scenario, solution)

warnings = [x for x in validation_result["regelVerletzungen"] if x["severity"] == "warning"]
errors = [x for x in validation_result["regelVerletzungen"] if x["severity"] == "error"]

if len(errors) > 0:
    print(f"the solution has {len(errors)} errors. It will not be accepted as a feasible solution. "
          f"See the error messages for details.")

elif len(warnings) > 0:
    print(f"the solution has {len(warnings)} warnings. It will be accepted as a feasible solution. However, it will "
          f"incur {validation_result['objectiveValue']} penalty points in the grader.")

