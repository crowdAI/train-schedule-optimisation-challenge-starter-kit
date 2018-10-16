###############################################
# set 'scenario' to the path to problem_instance
# set 'solution' to the path to your solution

# the data from solution_with_route_penalty contains evey route_section that is used in the solution.
# from this you can derive if and where your solution incurs route penalties.
###############################################
import json
import pandas as pd
from pandas.io.json import json_normalize

scenario = r"C:\devsbb\workspaces\train-schedule-optimisation-challenge-starter-kit\utils\07_V1.22_FWA.json"
solution = r"C:\devsbb\workspaces\train-schedule-optimisation-challenge-starter-kit\utils\model_07_V1.22_FWA_result.json"

with open(scenario) as fp, open(solution) as sol:
    scenario_content = json.load(fp)
    solution = json.load(sol)

fahrwege = list()
for route in scenario_content["routes"]:
    for route_path in route["route_paths"]:
        for route_section in route_path["route_sections"]:
            entry = dict(route=route["id"],
                         route_section_id=f"{route['id']}#{route_section['sequence_number']}",
                         penalty=route_section.get('penalty', 0))
            fahrwege.append(entry)

fahrwege_df = pd.DataFrame.from_dict(fahrwege)
solution_df = json_normalize(solution["train_runs"], record_path='train_run_sections')

solution_with_route_penalty = pd.merge(solution_df, fahrwege_df, how='inner', on=['route_section_id'])

print(solution_with_route_penalty['penalty'].sum())