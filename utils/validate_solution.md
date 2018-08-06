
# Individual solution validation

_Note: For full compatibility, use Python >= 3.6 to run this notebook._

This notebook explains how you can evaluate an individual solution to one of the [problem instances](problem_instances) without creating a whole submission.

This way, you can quickly and easily check if the solutions you calculated conform the the [business rules](documentation/business_rules.md) and you will also get a score for each solution, telling you how good it, as it will also calculate the [objective value](documentation/business_rules.md#objective-function) of this specific solution.

This makes frequent testing and tuning of your algorithm much easier than using the submission process.

__However: Please observe a limit of at most one (1) validation per minute in order not to overwhelm the service__

## Examples

_Note: The following code is also collected in_ [this](utils/validate_solution.py) _script_

Setup config:


```python
import requests
import translate
import json
from io import StringIO
import collections.abc
import os,sys,inspect

AUTH = ('MartyMcFly', 'Uranium-235')
SCENARIO_UPLOAD_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/uploadVerkehrsplanFile"
SOLUTION_VALIDATION_ENDPOINT = "https://fluxer.app.sbb.ch/backend/crowdai-validator/validateFile"
```

Specify the files to use. Validating a solution only makes sense when also specifying which problem instance the solution is intended for. So we specify both the problem instance and the solution. Both must be available as a JSON file.


```python
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

scenario = os.path.join(parentdir,'sample_files',"sample_scenario.json")
solution = os.path.join(parentdir,'sample_files',"sample_scenario_solution.json")

with open(scenario) as fp:
    scenario_content = json.load(fp)
```

We first read the file and send it to the translation. Translation translates the model from English to German, so our Solution Validator can understand it.


```python
scenario_content = ""
with open(scenario) as fp:
    scenario_content = json.load(fp)

scenario_content = translate.translate(scenario_content, translate.translate_to_ger)
```

We can now upload the solution to the service


```python
scenario_file = {"verkehrsplan": StringIO(json.dumps(scenario_content))}
upload_response = requests.post(SCENARIO_UPLOAD_ENDPOINT, files=scenario_file, auth=AUTH)
print(f"upload finished with status {upload_response}")
```

    upload finished with status <Response [200]>
    

We now read the solution file and translate it...


```python
solution_content = ""
with open(solution) as fp:
    solution_content = json.load(fp)

solution_content = translate.translate(solution_content, translate.translate_to_ger)
```

... in order to upload and validate the solution. The response from the validation is then translated again back into English


```python
solution_file = {"loesung": StringIO(json.dumps(solution_content))}
validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
print(f"validation finished with status {validation_response.status_code}")

response = validation_response.json()
validation_result = translate.translate(response, translate.translate_to_eng)
validation_result = translate.translate_message_word_for_word(validation_result)
```

    validation finished with status 200
    

Inspect the response. The rule violations are collected in the attribute `business_rules_violations`. They are grouped into `warnings` and `errors`

* `warnings` mean your solution violates some non-essential business rules. A common such case is if an event is scheduled too late (i.e. a delay). Solutions with warnings but no errors are accepted, but they may receive an imperfect score.
* `errors` means the solution violates an essential business rule. Solutions with errors are not accepted and scored just like a missing solution.

_Note:_ Some of the text might still be in German. Please use Google Translate in order to get some understanding.


```python
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

```

    
    There are 0 warnings and 0 errors
    
    

### Example: Warning "wrong Hash in solution"

The following solution has a wrong solution hash. This causes a `warning`, but this particular warning is irrelevant. Also, the solution is not penalized because of this. The `objective_value` of the solution is zero, which is perfect.

__you may safely ignore all solution-hash warnings in your solutions__


```python
solution = os.path.join(parentdir,'sample_files',"sample_scenario_solution_warningHash.json")

with open(solution) as fp:
    solution_content = json.load(fp)

solution_content = translate.translate(solution_content, translate.translate_to_ger)
solution_file = {"loesung": StringIO(json.dumps(solution_content))}
validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
print(f"validation finished with status {validation_response.status_code} \n")

response = validation_response.json()
validation_result = translate.translate(response, translate.translate_to_eng)
validation_result = translate.translate_message_word_for_word(validation_result)

warnings = [x for x in validation_result["business_rules_violations"] if x["severity"] == "warning"]
errors = [x for x in validation_result['business_rules_violations'] if x['severity'] == 'error']

print()
print(f"There are {len(warnings)} warnings and {len(errors)} errors" + "\n")

if len(errors) > 0:
    print(f"the solution has {len(errors)} errors. It will not be accepted as a feasible solution. "
        f"See the error messages for details.")

    print()
    print("Errors:")
    for x in errors:
        print("- "+x["message"])
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
```

    validation finished with status 200 
    
    
    There are 1 warnings and 0 errors
    
    
    the solution has 1 warnings. It will be accepted as a feasible solution. 
    
    Warnings:
    - Solution with VP-Label "SBB_challenge_sample_scenario_with_routing_alternatives" and problem_instance_hash "-1254734547" has a wrong Hash! Hash: 161193081, expected: 1538680897
    

### Example: Warning "delayed arrival"
The following solution again has a wrong solution hash, but again we ignore it.

__More importantly:__ Train 111 should arrive no later than 8:50:00 according to the [problem instance](sample_files/sample_scenario.json), but solution schedules it only at 8:51:08, which is 1.13 minutes too late. For this reason the solution is penalized with 1.13 `minutes_of_delay`, which is also its total `objective_value` (you can read up how the objective function is calculated [here](documentation/business_rules.md#objective-function)).


```python
solution = os.path.join(parentdir,'sample_files',"sample_scenario_solution_delayed_arrival.json")

with open(solution) as fp:
    solution_content = json.load(fp)

solution_content = translate.translate(solution_content, translate.translate_to_ger)
solution_file = {"loesung": StringIO(json.dumps(solution_content))}
validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
print(f"validation finished with status {validation_response.status_code} \n")

response = validation_response.json()
validation_result = translate.translate(response, translate.translate_to_eng)
validation_result = translate.translate_message_word_for_word(validation_result)

warnings = [x for x in validation_result["business_rules_violations"] if x["severity"] == "warning"]
errors = [x for x in validation_result['business_rules_violations'] if x['severity'] == 'error']

print()
print(f"There are {len(warnings)} warnings and {len(errors)} errors" + "\n")

if len(errors) > 0:
    print(f"the solution has {len(errors)} errors. It will not be accepted as a feasible solution. "
        f"See the error messages for details.")

    print()
    print("Errors:")
    for x in errors:
        print("- "+x["message"])
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

```

    validation finished with status 200 
    
    
    There are 2 warnings and 0 errors
    
    
    the solution has 2 warnings. It will be accepted as a feasible solution. 
    However, it will incur 1.1333333 penalty points in the grader.
    
    Warnings:
    - Solution with VP-Label "SBB_challenge_sample_scenario_with_routing_alternatives" and problem_instance_hash "-1254734547" has a wrong Hash! Hash: 1611930817, expected: 2080299070
    - Exit time 08:51:08 after exit_latest 08:50 for Train run sections with FAB-Id "111#14" and Section Marker "C" in fA "111"
    

### Example: Errors "early departure" and "resource occupation conflict"

This solution has actual _errors_. It will _not_ be accepted as a feasible solution by the grader. There are three errors:
* The service intentions 111 and 113 occupy both occupy resource 'AB' at the same time, namely
 - 111 on its route section with sequence number 3 (route section id '111#3') from 07:50:00 to 08:20:53
 - 113 on its route section number 1 from 07:50:00 to 07:50:53
 
* The same service intentions also conflict each other on route sections 111#3 and 113#4. This is listed as a separate conflict

* Service intention 111 enters route section 111#3 (its first route section) at 07:50:00. This is earlier than the `earliest entry` of 08:20:00 specified in the service intention.


```python
solution = os.path.join(parentdir,'sample_files',"sample_scenario_solution_early_entry.json")

with open(solution) as fp:
    solution_content = json.load(fp)

solution_content = translate.translate(solution_content, translate.translate_to_ger)
solution_file = {"loesung": StringIO(json.dumps(solution_content))}
validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
print(f"validation finished with status {validation_response.status_code} \n")

response = validation_response.json()
validation_result = translate.translate(response, translate.translate_to_eng)
validation_result = translate.translate_message_word_for_word(validation_result)

warnings = [x for x in validation_result["business_rules_violations"] if x["severity"] == "warning"]
errors = [x for x in validation_result['business_rules_violations'] if x['severity'] == 'error']

print()
print(f"There are {len(warnings)} warnings and {len(errors)} errors" + "\n")

if len(errors) > 0:
    print(f"the solution has {len(errors)} errors. It will not be accepted as a feasible solution. "
        f"See the error messages for details.")

    print()
    print("Errors:")
    for x in errors:
        print("- "+x["message"])
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
```

    validation finished with status 200 
    
    
    There are 1 warnings and 3 errors
    
    the solution has 3 errors. It will not be accepted as a feasible solution. See the error messages for details.
    
    Errors:
    - Occupancy conflict (Blocking resource) Release time[s] 30, Resource: "AB", fAs: "111" / "113", FABs: "111#3" / "113#1", Times entry-exit: 07:50-08:20:53 / 07:50-07:50:53
    - Occupancy conflict (Blocking resource) Release time[s] 30, Resource: "AB", fAs: "111" / "113", FABs: "111#3" / "113#4", Times entry-exit: 07:50-08:20:53 / 07:50:53-07:51:25
    - Entry time 07:50 before entry_earliest 08:20 for Train run sections with FAB-Id "111#3" and Section Marker "A" in fA "111"
    
    Warnings:
    - Solution with VP-Label "SBB_challenge_sample_scenario_with_routing_alternatives" and problem_instance_hash "-1254734547" has a wrong Hash! Hash: 1611930817, expected: 460224476
    
