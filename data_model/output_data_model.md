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

Let's go through them. You may use this [sample solution](sample_files\sample_scenario_with_routing_alternatives_solution.json) as a reference.

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

For example, the reference [sample solution](dhttps://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives_solution.json) to the [sample instance](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario_with_routing_alternatives.json) looks as follows:

The solution picks the following routes for the two _service_intentions_:

![](data_model/img/solution_routes.png)

This results in the following _train_run_sections_ for the _service_intentions_:

![](data_model/img/solution_sections_and_times.png)