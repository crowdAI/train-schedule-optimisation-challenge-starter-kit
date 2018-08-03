import requests
import translate
import json
from io import StringIO
import collections.abc

AUTH = ('MartyMcFly', 'Uranium-235')
SCENARIO_UPLOAD_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/uploadVerkehrsplanFile"
SOLUTION_VALIDATION_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/validateFile"

scenario = "../sample_files/sample_scenario.json"
solution = "../sample_files/sample_scenario_solution.json"


def do_loesung_validation(scenario, solution):

    # upload scenario first (may not be available in the store)
    # read in scenario_content
    scenario_content = ""
    with open(scenario) as fp:
        scenario_content = json.load(fp)

    scenario_content = translate.translate(scenario_content, translate.translate_to_ger)

    scenario_file = {"verkehrsplan": StringIO(json.dumps(scenario_content))}
    upload_response = requests.post(SCENARIO_UPLOAD_ENDPOINT, files=scenario_file, auth=AUTH)
    print(f"upload finished with status {upload_response}")


    # now we can validate
    solution_content = ""
    with open(solution) as fp:
        solution_content = json.load(fp)

    solution_content = translate.translate(solution_content, translate.translate_to_ger)
    solution_file = {"loesung": StringIO(json.dumps(solution_content))}
    validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
    print(f"validation finished with status {validation_response}")

    response = validation_response.json()
    translated_response = translate.translate(response, translate.translate_to_eng)
    return translated_response



if __name__ == "__main__":
    validation_result = do_loesung_validation(scenario, solution)
    print(validation_result)

    warnings = [x for x in validation_result["business_rules_violations"] if x["severity"] == "warning"]
    errors = [x for x in validation_result["business_rules_violations"] if x["severity"] == "error"]

    if len(errors) > 0:
        print(f"the solution has {len(errors)} errors. It will not be accepted as a feasible solution. "
            f"See the error messages for details.")

    elif len(warnings) > 0:
        print(f"the solution has {len(warnings)} warnings. It will be accepted as a feasible solution. However, it will "
            f"incur {validation_result['objective_value']} penalty points in the grader.")