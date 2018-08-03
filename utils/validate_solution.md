
# Individual solution validation via the REST-API of the Solution Validator Service

_Note: For full compatibility, use Python >= 3.6 to run this notebook._

The REST-API of the Solution Validator can be used to check
* whether a solution respects all required [business rules](documentation/business_rules.md) (and if not, where exactly the violoations are)
* the [objective value](documentation/business_rules.md#objective-function) of a solution

It thus provides a shortcut to the complete submission-procedure (where you are required to submit a full set of solutions for all problem instances) to validate individual solutions.

This makes frequent testing and tuning of your algorithm much easiere.

_However: Please observe a limit of at most one (1) validation per minute in order not to overwhelm the service_

## Examples

_Note: The following code is also collected in_ [this](validate_solution.py) _script_

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

scenario_content = ""
with open(scenario) as fp:
    scenario_content = json.load(fp)
```

    C:\devsbb\TMS\train-schedule-optimisation-challenge-starter-kit\utils
    

We first read the file and send it to the translation. Translation translates the model from English to German. 


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
print(f"validation finished with status {validation_response}")

response = validation_response.json()
validation_result = translate.translate(response, translate.translate_to_eng)
```

    validation finished with status <Response [200]>
    

Inspect the response. The rule violations are collected in the attribute `business_rules_violations`. Some of the strings might still be in German. Please use Google Translate in order to get some undestanding.


```python
print(validation_result)

warnings = [x for x in validation_result["business_rules_violations"] if x["severity"] == "warning"]
errors = [x for x in validation_result["business_rules_violations"] if x["severity"] == "error"]
```

    {'business_rules_violations': [{'severity': 'warning', 'message': 'Lösung mit VP-Label "SBB_challenge_sample_scenario_with_routing_alternatives" und VP-Hash "-1254734547" hat einen falschen Hash! Hash: 1611930817, erwartet: 1538680897'}], 'solution_hash': 1611930817, 'objective_value': 0.0, 'details': {'minutes_of_delay': '0.0', 'route_penalty': '0.0'}, 'request_uuid': None}
    

### Example: Warning "wrong Hash in solution"

The following solution has a wrong solution hash. This causes a warning, but it is irrelevant. Also, the solution is not penalized because of this. objValue is zero.

__you may safely ignore all solution-hash warnings in your solutions__


```python
solution = "samples/sample_scenario_simple_solution_warningHash.json"
solution_file = {"loesung": open(solution, 'rb')}
validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
validation_result = validation_response.json()

assert len(validation_result["regelVerletzungen"]) == 1

```

### Example: Warning "delayed arrival" and "wrong Hash in solution"
The following solution has a wrong solution hash. This causes a warning, but it is irrelevant. 
Train 111 should arrive no later than 8:50:00, but solution return 8:51:08, which is 1.13 minutes too late. For this reason the solution.

__you may safely ignore all solution-hash warnings in your solutions__


```python
solution = os.path.join(parentdir,'sample_files',"sample_scenario_solution_delayed_arrival.json")

solution_content = ""
with open(solution) as fp:
    solution_content = json.load(fp)

solution_content = translate.translate(solution_content, translate.translate_to_ger)
solution_file = {"loesung": StringIO(json.dumps(solution_content))}
validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
print(f"validation finished with status {validation_response}")

response = validation_response.json()
validation_result = translate.translate(response, translate.translate_to_eng)

from pprint import pprint
pprint(validation_result)
```

    validation finished with status <Response [200]>
    {'business_rules_violations': [{'message': 'Lösung mit VP-Label '
                                               '"SBB_challenge_sample_scenario_with_routing_alternatives" '
                                               'und VP-Hash "-1254734547" hat '
                                               'einen falschen Hash! Hash: '
                                               '1611930817, erwartet: 2080299070',
                                    'severity': 'warning'},
                                   {'message': 'Austrittszeit 08:51:08 nach ausMax '
                                               '08:50 für Zugfahrtabschnitt mit '
                                               'FAB-Id "111#14" und '
                                               'Abschnittskennzeichen "C" in fA '
                                               '"111"',
                                    'severity': 'warning'}],
     'details': {'minutes_of_delay': '1.1333333', 'route_penalty': '0.0'},
     'objective_value': 1.1333333,
     'request_uuid': None,
     'solution_hash': 1611930817}
    

### Example: Errors "early departure" and "resource occupation conflict"

This solution has actual _errors_. It will _not_ be accepted as a feasible solution by the grader. There are two errors:
* The service intentions "EC/163-001/PF-SA" and "IC/913-001/PF-SA" overtake each other on the route section PF_SA/IC#17. This (obviously) violates the separation constraints for the associated resource "MELS_SA"
* Service Intention EC/163-001/PF-SA enters into route section PF_SA/IC#1 at 09:00:30. This is _before_ the earliest allowed entry time of 09:02:30.

Note: In addition, there is also a warning because train IC/913-001/PF-SA arrives too late.


```python
solution = "samples/sample_scenario_simple_solution_errors.json"
solution_file = {"loesung": open(solution, 'rb')}
validation_response = requests.post(SOLUTION_VALIDATION_ENDPOINT, files=solution_file, auth=AUTH)
validation_result = validation_response.json()
errors = [x for x in validation_result['regelVerletzungen'] if x['severity'] == 'error']

print(f"There are {len(errors)} errors" + "\n")

for x in validation_result["regelVerletzungen"]:
    if x["severity"] == 'error':
        print(x["message"] + '\n')
```

    There are 2 errors
    
    Belegungskonflikt (Zugfolgezeit gleiche Richtung: MELS_SA), Zugfolgezeit[s]: 180, Ressource: "MELS_SA", fAs: "EC/163-001/PF-SA" / "IC/913-001/PF-SA", FABs: "PF_SA/IC#17" / "PF_SA/IC#17", Zeiten ein-aus: 09:33:36.600-09:35:39 / 09:00:36.600-09:40:39
    
    Eintrittszeit 09:00:30 vor einMin 09:02:30 für Zugfahrtabschnitt mit FAB-Id "PF_SA/IC#1" und Abschnittskennzeichen "PF" in fA "EC/163-001/PF-SA"
    
    
