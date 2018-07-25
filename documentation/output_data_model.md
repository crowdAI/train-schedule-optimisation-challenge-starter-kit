This document describes the data model in which the _solutions_ to the problem instances have to be delivered.

# A Note on translation from and to German
Lke for the _problem_instances_, our model for the output, i.e. a solution to a problem instance, is in German. You must submit solutions in German.

However: to help you work with English terminology internally, we provide translation helper scripts that you can use to translate a problem instance into English and to translate an English solution into the German terminology we require.

The translation script is [here](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/utils/translate.py).

# Data Model of a solution

A _solution_ to a _problem_instance_ has the following elements:
* problem_instance_label (verkehrsplanLabel)
* problem_instance_hash (verkehrsplanHash)
* hash
* train_runs (zugfahrten)
* [properties]

Let's go through them. You may use this [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json) as a reference.

# problem_instance_label (verkehrsplanLabel)
The _label_ of the _problem_instance_ that this solution is intended for.

# problem_instance_hash (verkehrsplanHash)
The _hash_ of the _problem_instance_ that this solution is intended for. This is the actual identifier that the grader will use to check if your solution is valid and compute its score. It is imperative that this field is filled correctly, otherwise the grader will not be able to match your solution to a problem instance.

# hash
This field can be used to provide a hash-value for the _solution_. However, while the field is required, its value is not really used afterwards. You may enter any fixed integer, e.g. 42, for every _solution_ you submit.

# train_runs (zugfahrten)
This is the actual 'meat' of the _soulution_. Namely, it contains for each service_intention_ an ordered list of _train_run_sections_ (zugfahrtabschnitte) that describe a simple path through the route_graph for this train. For each _train_run_section_ (zugfahrtabschnitt) it provides a time-of-day for the _entry_time_ (ein) and the _exit_time_ (aus).

In other words, a solution means
* picking exactly one of all possible routes for this train, and
* assigning a time to each _event_ (entry into and exit from _route_sections_)

For example, the reference [sample solution](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json) to the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) looks as follows:

The solution picks the following routes for the two _service_intentions_:

![](data_model/img/solution_routes.png)

This results in the following _train_run_sections_ for the _service_intentions_:

![](data_model/img/solution_sections_and_times.png)

Let's look at the formal model for _train_run_sections_

## train_run_section (zugfahrtabschnitt)
A _train_run_section_ is built as follows

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| entry_time (ein)   | time of day in HH24:MM:SS                         | event time for the _entry_event_ into this _train_run_section_. <br>__Note__: This time must always be equal to the _exit_time_ of the previous _train_run_section_    |
| exit_time (aus)   | time of day in HH24:MM:SS                         | event time for the _exit_event_ from this _train_run_section_. <br>__Note__: This time must always be equal to the _entry_time_ into the next _train_run_section_    |
| route (fahrweg)   | text                         | reference to the _id_ of the _route_ for this _service_intention_ |
| route_section (fahrwegabschnitt)   | text                         | reference to the _id_ of the particular _route_section_ that this _train_run_section_ represents |
| route_path (abschnittsfolge)   | text                         | reference to the _id_ of the _route_path_ in which the _route_section_ represented by this _train_run_section_ is located |
| sequence_number (reihenfolge)   | positive Integer                         | an ordering for the _train_run_sections_. Necessary because the JSON specification does not guarantee that the order in the file is respected when it is deserialized. |
| section_requirement (abschnittsvorgabe)   | text                         | must be set to the corresponding _section_requirement_ of the service intention if this requirement is to be satisfied on this particular _train_run_section_. <br> __Note:__  We guarantee that the route graphs in our problem instances are such that whatever route you happen to choose, you will pass each required _section_marker_ exactly once. Actually, we even guarantee, that you will pass them in the same sequence as required by the _service_intention_. <br>So once you have picked your route, you can just check if the _route_section_ referenced by this _train_run_section_ has a _section_marker_ that also occurs in the _service_intention_. If so, put this _section_marker_ in this field.

# properties
An optional field that can be used to collect information/statistics on the solution. You do not need to submit any properties. Omit this field.