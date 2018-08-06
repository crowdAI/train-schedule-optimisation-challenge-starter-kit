import requests
import translate
import json
from io import StringIO
import collections.abc
import os,sys,inspect

AUTH = ('MartyMcFly', 'Uranium-235')
SCENARIO_UPLOAD_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/uploadVerkehrsplanFile"
SOLUTION_VALIDATION_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/validateFile"

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

scenario = os.path.join(parentdir,'sample_files',"sample_scenario.json")
solution = os.path.join(parentdir,'sample_files',"sample_scenario_solution.json")

def do_loesung_validation(scenario, solution):

    # upload scenario first (may not be available in the store)
    # read in scenario_content
    scenario_content = ""
    with open(scenario) as fp:
        scenario_content = json.load(fp)

    scenario_content = translate.translate(scenario_content, translate.translate_to_ger)

    scenario_file = {"verkehrsplan": StringIO(json.dumps(scenario_content))}
    upload_response = requests.post(SCENARIO_UPLOAD_ENDPOINT, files=scenario_file, auth=AUTH)
    print(f"upload finished with status {upload_response.status_code}")


    # now we can validate
    solution_content = ""
    with open(solution) as fp:
        solution_content = json.load(fp)

    solution_content = translate.translate(solution_content, translate.translate_to_ger)
    solution_file = {"loesung": StringIO(json.dumps(solution_content))}
    validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
    print(f"validation finished with status {validation_response.status_code}")

    response = validation_response.json()
    validation_result = translate.translate(response, translate.translate_to_eng)
    validation_result = translate.translate_message_word_for_word(validation_result)
    return validation_result


if __name__ == "__main__":
    validation_result = do_loesung_validation(scenario, solution)
    # print(validation_result)

    warnings = [x for x in validation_result["business_rules_violations"] if x["severity"] == "warning"]
    errors = [x for x in validation_result["business_rules_violations"] if x["severity"] == "error"]

    print()
    print(f"There are {len(warnings)} warnings and {len(errors)} errors" + "\n")

    if len(errors) > 0:
        print(f"the solution has {len(errors)} errors. It will not be accepted as a feasible solution. "
            f"See the error messages for details.")
    
        print()
        print("Errors:")
        for x in errors:
            print("- "+x["message"])
            # print(x["message_original"])
        print()
        print("Warnings:")
        for x in warnings:
            print("- "+x["message"])
        

    elif len(warnings) > 0:
        print()
        print(f"the solution has {len(warnings)} warnings. It will be accepted as a feasible solution. ")
        if validation_result['objective_value'] > 0.0:
            print(f"However, it will incur {validation_result['objective_value']} penalty points in the grader.")
        
        print()
        print("Warnings:")
        for x in warnings:
            print("- "+x["message"])
            # print(x["message_original"])