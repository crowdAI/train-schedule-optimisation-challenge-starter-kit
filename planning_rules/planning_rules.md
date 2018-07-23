This document describes the rules that have to be observed in order that a _solution_ to a _problem instance_ is considered valid.

Your solver will need to make sure that the solutions it produces observe these rules.

We categorize the rules roughly in two groups:
* _Consistency rules_, which mostly check technical conformity to the data model
* _Planning rules_,  which represent the actual business rules involved in generating a timetable

__Remember you have to submit solutions in the _German_ format.__ If you prefer to work with English terms internally, you may use the [translation script](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/utils/translate.py) to translate an English solution to a German one before submitting.

# Concistency Rules

| Rule Name         | Rule Definition   | Remarks |
| -------           | -----             | ----    |
| verkehrsplanHash (problem_instance_hash)       | the fiel _verkehrsplanHash_ (_problem_instance_hash_) is present in the solution                           | |
| each train is scheduled       | For every _funktionaleAngebotsbeschreibung_ (_service_intention_) in the _verkehrsplan_ (_problem_instance_), there is exactly one _zugfahrt_ (_train_run_) in the solution  | |
| The _sequence_numbers_ form an ordering of the _train_run_sections_ by their _sequence_numbers_       | For every _zugfahrt_ (_train_run_), the field _reihenfolge_ (_sequence_number_) can be ordered as a strictly increasing sequence of positive integers  | in other words, the _sequence_numbers_ are _unique_ among all _train_run_sections_ for a _train_run_. <br>Typically, it is natural to also list the _train_run_sections_ in increasing order in the JSON file, such as is the case for the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json). However, strictly speaking de-/serialization from/to JSON need not preserve orders. Having an explicit _sequence_number_ is advisable.  |
| Reference a valid _route_, _route_path_ and _route_section_      | each _zugfahrtabschnitt_ (_train_run_section_) references the _fahrweg_ (_route_) for this _service_intention_, and the correct _abschnittsfolge_ (_route_path_), and the correct fahrwegabschnitt (_route_section_)  | |
| Same order in _train_run_sections_ as in _route_sections_      | If two _train_run_sections_ A and B are adjacent according to their _sequence_number_, say B directly follows A, then the associated _route_sections_ A' and B' must also be adjacent in the route graph, i.e. B' directly follows A'.  | In other words, the _train_run_sections_ form a path (linear subgraph) in the route graph. Check the illustrations in the [Output Data Model description](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/2cd85f53715261cf6a71d319e99d0b5c577ffbab/data_model/output_data_model.md). |
| reference valid _section_requirement_      | a _zugfahrtabschnitt_ (_train_run_section_) references an _abschnittsvorgabe_ (_section_requirement_) if and only if this _section_requirement_ is listed in the _service_intention_.  | for example, in the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json), the _train_run_sections_ for _service_intention_ 111 have references to the _section_requirements_ A, B and C. But the _train_run_sections_ for _service_intention_ 113 only reference _section_requirements_ A and C, even though both _service_intentions_ have the same _route_. This is because in the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) the _service_intention_ for 113 does not have a _section_requirement_ for the _section_marker_ 'B', but only for 'A' and 'C'|
| consistent _ein_ (_entry_time_) and _aus_ (_exit_time_) times      | for each pair of immediately subsequent _train_run_sections_, say S1 followed by S2, we have S1._exit_time_ = S2._entry_time_ | recall the ordering of the _train_run_sections_ is given by their _sequence_number_ attribute|

<br>

# Planning Rules

| Rule Name         | Rule Definition   | Remarks |
| -------           | -----             | ----    |
| Time windows for _earliest_-requirements     | If a _section_requirement_ that specifies an _earliest_entry_ and/or _earliest_exit_ time then the event times for the _entry_event_ and/or _exit_event_ on the corresponding _train_run_section_ __MUST__ be >= the specified time          | for example, in the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) for _service_intention_ 111 there is a requirement for _section_marker_ 'A' with an _earliest_entry_ of 08:20:00. Correspondingly, in the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json) the corresponding _entry_event_ is scheduled at precisely 08:20:00. This is allowed. But 08:19:59 or earlier would not be allowed; such a solution would be rejected.|
| Time windows for _latest_-requirements     | If a _section_requirement_ that specifies a _latest_entry_ and/or _latest_exit_ time then the event times for the _entry_event_ and/or _exit_event_ on the corresponding _train_run_section_ __SHOULD__ be <= the specified time <br> If the scheduled time is later than required, the solution will still be accepted, however it will be penalized by the objective function, see below.          | for example, in the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) for _service_intention_ 111 there is a requirement for _section_marker_ 'A' with a _latest_entry_ of 08:30:00. In the [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json) the corresponding _entry_event_ is scheduled at 08:20:00. Any time not later than 08:30:00 would satisfy this requirement. Any time >= 08:30:01 would incur a lateness penalty.
| Minimum section time     | For each _train_run_section_ the following holds: <br> t<sub>exit</sub> - t<sub>entry</sub> >= minimum_running_time + min_stopping_time, where <br> t<sub>entry</sub>, t<sub>exit</sub> are the entry and exit times into this _train_run_section_, minimum_running_time is given by the _route_section_ corresponding to this _train_run_section_ and min_stopping_time is given by the _section_requirement_ corresponding to this _train_run_section_ or equal to 0 (zero) if no _section_requirement_ is associated to this section, or the _section_requirement_ does not specify a min_stopping_time. | |
| Resource Occupations     | Let S1 and S2 be two _train_run_sections_ belonging to _distinct_ service_intentions T1, T2 and such that the associated _route_sections_ occupy at least one common resource.  Without loss of generality, assume that T1 enters section S1 before T2 enters S2, i.e. <br> t<sub>S1, entry</sub> < t<sub>S2, entry</sub>. <br> Then for _each commonly occupied resource_ R, the following must hold: <br> t<sub>S2, entry</sub> >= t<sub>S1, exit</sub> + d<sub>R, release</sub>, <br> where d<sub>R, release</sub> is the _release_time_ (_freigabezeit_) of resource R| In prose, this means that _if_ a train T1 starts occupying a resource R before train T2, then T2 has to wait until T1 releases it (plus the release time of the resource) before it can start to occupy it. <br><br>This rule explicitly need _not_ hold between train_run_sections _of the same train_. The problem instances are infeasible if you require this separation of occupations also among _train_run_sections_ of the same train.
| Connections     | Let C be a connection defined in _service_intention_ SI1 onto _service_intention_ SI2 with _section_marker_ M and let d<sub>C</sub> be the connection's _min_connection_time_. <br> Let S1 be the _train_run_section_ for SI1 where the connection will take place (i.e. the section which has 'M' in the _section_requirement_ attribute) and S2 the same for SI2. Then the following must hold:<br> t<sub>S2, exit</sub> - t<sub>S1, entry</sub> >= d<sub>C</sub>, <br> where, again, t<sub>S1, entry</sub> denotes the time for the _entry_event_ into _train_run_section_ S1 and t<sub>S2, exit</sub> the time for the _exit_event_ from _train_run_section_ S2. | 

## Ojective Function
The objective function is used by the grader to determine how good your solution is. We give a more exact formula below, but basically it is calculated as the __weighted sum of all delays plus the sum of routing penalties__.
A _delay_ in this context means a violation of a _section_requirement_ with an _exit_latest_ or _entry_latest_ time, i.e. these  events are scheduled too late. Each such violation is multiplied by its _entry_delay_weight_/_exit_delay_weight_ and then summed up to get the total delay penalties. <br>

The best possible objective value a solution can obtain is 0 (zero). A value > 0 means some _latest_entry_/_latest_exit_ _section_requirement_ is not satisfied in the solution, or a route involving _routing_sections_ with _penalty_ > 0 was chosen.

The "formula", if you will, for the objective function is as follows:

```math
\frac{1}{60} \cdot \Big( \sum_{\textrm{SI, SR}} \textrm{entry\_delay\_weight}_{SR} \; \cdot \; max(0, t_{entry} - \textrm{entry\_latest}_{SR}) \; + \; \textrm{exit\_delay\_weight}_{SR} \; \cdot \; max(0, t_{exit} - \textrm{exit\_latest}_{SR}) \Big) + \sum_{\textrm{TRS}} \textrm{penalty}_{\textrm{route\_section}_\textrm{TRS}}
```
where:
* The first sum is taken over all _service_intentions_ $`SI`$ and all _section_requirements_ $`SR`$ therein,
* The second sum is taken over all _train_run_sections_ $`TRS`$,
* $`\textrm{entry\_delay\_weight}_{SR}`$ stands for the _entry_delay_weight_ specified for this particular _section_requirement_. If the _section_requirement_ does not specify an _entry_delay_weight_, then it is assumed to be = 0.
* $`t_{entry}`$ denotes the scheduled time in the solution for the _entry_event_ into the _train_run_section_ where this _section_requirement_ is satisfied,
* $`\textrm{entry\_latest}_{SR}`$ denotes the desired latest entry time specified in the field _entry_latest_ of the _section_requirement_<br> _Note_: If the _section_requirement_ does not specify an _entry_latest_, then it is assumed to be $`+\infty`$, i.e. the $`max`$ will be zero and the term ignored.

_Note:_ The normalization constant $`1/60`$ for the delay penalty term means that 60s of delay will incur 1 penalty point (provided all _delay_weight_ are equal to 1. In other words, we count the delay 'minutes'.

### Example for delay penalties
In this example, the _service_intention_ has the following three _section_requirements_:
* _entry_earliest_ = 8:50 for _section_marker_ A
__ToDo: Hier weiter. Bilder einfügen__