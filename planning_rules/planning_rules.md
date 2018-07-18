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
| same order in _train_run_sections_ as in _route_sections_      | If two _train_run_sections_ are adjacent accoring to their _sequence_number_, then the associated _route_sections_ must also be adjacent in the route graph.  | In other words, the _train_run_sections_ form a path (linear subgraph) in the route graph. <br> Or, in yet other terms, the train must travel through the route graph 'without jumps' |
| reference valid _section_requirement_      | a _zugfahrtabschnitt_ (_train_run_section_) references an _abschnittsvorgabe_ (_section_requirement_) if and only if this _section_requirement_ is listed in the _service_intention_.  | for example, in the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json), the _train_run_sections_ for _service_intention_ 111 have references to the _section_requirements_ A, B and C. But the _train_run_sections_ for _service_intention_ 113 only reference _section_requirements_ A and C, even though both _service_intentions_ have the same _route_. This is because in the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) the _service_intention_ for 113 does not have a _section_requirement_ for the _section_marker_ 'B', but only for 'A' and 'C'|
| consistent _ein_ (_entry_time_) and _aus_ (_exit_time_) times      | for each pair of immediately subsequent _train_run_sections_, say S1 followed by S2, we have S1._exit_time_ = S2._entry_time_ | recall the ordering of the _train_run_sections_ is given by their _sequence_number_ attribute|

# Planning Rules

| Rule Name         | Rule Definition   | Remarks |
| -------           | -----             | ----    |
| Time windows for _earliest_-requirements     | If a _section_requirement_ that specifies an _earliest_entry_ and/or _earliest_exit_ time then the event times for the _entry_event_ and/or _exit_event_ on the corresponding _train_run_section_ __MUST__ be >= the specified time          | for example, in the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) for _service_intention_ 111 there is a requirement for _section_marker_ 'A' with an _earliest_entry_ of 08:20:00. Correspondingly, in the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json) the corresponding _entry_event_ is scheduled at precisely 08:20:00. This is allowed. But 08:19:59 or earlier would not be allowed. Such a solution would be rejected.|
| Time windows for _latest_-requirements     | If a _section_requirement_ that specifies a _latest_entry_ and/or _latest_exit_ time then the event times for the _entry_event_ and/or _exit_event_ on the corresponding _train_run_section_ __SHOULD__ be <= the specified time <br> If the scheduled time is later than required, the solution will still be accepted, however it will be penalized by the objective function, see below.          | for example, in the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) for _service_intention_ 111 there is a requirement for _section_marker_ 'A' with a _latest_entry_ of 08:30:00. Correspondingly, in the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json) the corresponding _entry_event_ is scheduled at 08:20:00. Any time not later than 08:30:00 would satisfy this requirement. Any time >= 08:30:01 would incur a lateness penalty.

## Ojective Function