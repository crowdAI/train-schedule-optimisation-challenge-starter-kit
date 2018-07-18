This document describes the rules that have to be observed in order that a _solution_ to a _problem instance_ is considered valid.

Your solver will need to make sure that the solutions it produces observe these rules.

We categorize the rules roughly in two groups:
* _Consistency rules_, which mostly check technical conformity to the data model
* _Planning rules_,  which represent the actual business rules involved in generating a timetable

__Remember you have to submit solutions in the _German_ format.__ You may use the [translation script](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/utils/translate.py) to translate an English solution to a German one.

# Concistency Rules

| Rule Name         | Rule Definition   | Remarks |
| -------           | -----             | ----    |
| verkehrsplanHash (problem_instance_hash)       | the fiel _verkehrsplanHash_ (_problem_instance_hash_) is present in the solution                           | |
| each train is scheduled       | For every _funktionaleAngebotsbeschreibung_ (_service_intention_) in the _verkehrsplan_ (_problem_instance_), there is exactly one _zugfahrt_ (_train_run_) in the solution  | |
| strictly increasing _sequence_numbers_       | For every _zugfahrt_ (_train_run_), the field _reihenfolge_ (_sequence_number_) can be ordered as a strictly increasing sequence of positive integers  | in other words, the values are _unique_ among all _train_run_sections_ for a _train_run_ |
| reference valid _route_, _route_path_ and _route_section_      | each _zugfahrtabschnitt_ (_train_run_section_) references the _fahrweg_ (_route_) for this _service_intention_, and the correct _abschnittsfolge_ (_route_path_), and the correct fahrwegabschnitt (_route_section_)  | |
| reference valid _section_requirement_      | a _zugfahrtabschnitt_ (_train_run_section_) references an _abschnittsvorgabe_ (_section_requirement_) if and only if this _section_requirement_ is listed in the _service_intention_.  | for example, in the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json), the _train_run_sections_ for _service_intention_ 111 have references to the _section_requirements_ A, B and C. But the _train_run_sections_ for _service_intention_ 113 only reference _section_requirements_ A and C, even though both _service_intentions_ have the same _route_. This is because in the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) the _service_intention_ for 113 does not have a _section_requirement_ for the _section_marker_ 'B'|
| consistent _ein_ (_entry_time_) and _aus_ (_exit_time_) times      | for each pair of immediately subsequent _train_run_sections_, say S1 followed by S2, we have S1._exit_time_ = S2._entry_time_ | recall the ordering of the _train_run_sections_ is given by their _sequence_number_ attribute|

# Planning Rules

## Ojective Function