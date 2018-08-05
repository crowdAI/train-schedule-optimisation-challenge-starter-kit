# A Worked Example

Let us build a solution to the [sample instance](sample_files/sample_scenario.json) from the ground up. 

You do not need to be familiar with the data models yet or the business rules, but we recommend that you keep the following documents handy while working through the example

* The description of the [problem instance data model](documentation/input_data_model.md)
* The description of the [solution data model](documentation/output_data_model.md)
* The definition of the twelve [business rules](documentation/business_rules.md) that a solution must satisfy

## The sample instance
We study what is contained in the [sample isntance](sample_files/sample_scenario.json)
### Service intentions
There are two service intentions, for trains 111 and 113.

![](documentation/img/worked_example_service_intentions.png)

* service intention 111 has three _section_requirements_, for _section_markers_ 'A', 'B' and 'C'. 
* service intention 113 has only two _section_requirements_, for _section_markers_ 'A' and 'C'.

We notice train 111 must circulate sometime between 8:20, its earliest possible start time at its first _section_requirement_, and 8:50, its latest desired exit time at its last _section_requirement_. Train 111 also has a _section_requirement_ at some intermediate section 'B', where it wants to stop for a minimum of 3 minutes and exit that section no earlier than 8:30. Think of this as a commercial stop of the train: if the timetable in 'B' says "Departure at 8:30", then the passengers wanting to catch the train in 'B' would be unhappy if it left at 8:25, or anytime before 8:30. Therefore, it makes sense to require a departure "no earlier than" 8:30. This is what the _exit_earliest_ for _section_requirement_ B ensures.

Likewise, train 113 must circulate sometime between 7:50 and 8:16 (so actually earlier than train 111). It has no other requirements.

Also, note that neither train specifies any connections that would have to be observed. All we have to worry about are the _earliest_ and _latest_ time requirements. That can't be too hard?

### Routes
We recall from the [short introduction](documentation#a-very-quick-introduction-to-our-timetabling-problem) that producing a solution amounts to

* picking exactly one of the possible routes for each train, i.e. __selecting a path from a source to a sink node__ in the route graph
* then assign times to all events (nodes) on this path (such that all tweve [business rules](documentation/business_rules.md) are satisfied)

We also recall that the __route graphs are always directed and acyclic grpahs__.

So, what are the possible routes for the two services? We will see in the discussion of the [problem instance data model](documentation/input_data_model.md#routes) how to derive the graph structure from the JSON. For the purpose of this example, let us just pretend we already knew that the two route graphs for service intentions 111 and 113 are actually identical and look as follows:

#### Route graphs for _service_intentions_ 111 and 113
_Hint:_ you may use the [route graph utility script](utils/route_graph.py) to produce the route graphs as a [networkx](https://networkx.github.io/) directed graph and that should produce the same graphs as in these pictures.

![](documentation/img/worked_example_route_graph.png)

Note that the fact that they have identical route graphs means the trains actually have the same travel path. In the "real world" this would mean they travel along the same pyhsical tracks.

## Building a Solution
We now start to build the solution. The following steps are just an example; it is neither the only nor a very intelligent way to go about this problem. But it works for simple examples such as this one. We will follow these steps:

1. select a route for each service intention
2. Take a first shot at assigning times to all events along the chosen routes
3. check if we satisfy all [business rules](documentation/business_rules.md)
    1. If yes, we are done
    2. If not, adjust the event times and check again

### 1. Select a route
We must choose a path from a source node to a sink node in the route graph.

We notice that no _route_section_ has a positive _penalty_. If there were any such _route_sections_, we might try to avoid them when choosing our first route. But in this case, it really does not matter - all routes are equally 'desirable'. Our choice is as follows (we list the _sequence_numbers_ of the _route_sections_):
* train 111 shall travel over _route_sections_ # 3 -> 4 -> 5 -> 6 -> 10 -> 13 -> 14
* train 113 shall travel over _route_sections_ # 1 -> 4 -> 5 -> 6 -> 10 -> 13 -> 14

![](documentation/img/worked_example_selected_routes.png)

### 2. Initial Assignment of Event Times
With the route choice above, we have the following paths for the two trains. Each entry and exit event (i.e. each _node_) needs to be assigned a time. In the language of the [solution data model](documentation/output_data_model.md), the arcs in the following graph are called _train_run_sections_.
*******************

![](documentation/img/worked_example_raw_train_run_sections.png)
******************
Our first inclination for assigning the event times is to schedule every event as early as possible. Specifically, 

* let the trains start as early as possible
* let them spend only the required _minimum_running_time_ on each section

To do that, it helps to add some more information to the _train_run_sections_ (i.e. the arcs) in the graph:
* the _section_marker_ of the associated _route_sections_, if there is one
* the _minimum_running_time_ of the associated _route_section_

![](documentation/img/worked_example_minimum_running_time_and_section_markers.png)

Now the earliest possible starting times for the trains are given by the _entry_earliest_ time of the first _section_requirement_ (by the way: it is a general convention of all problem instances, that the first _setion_requirement_ always has an _entry_earliest_, and the last _section_requirement_ always has an _exit_latest_)

In our case, this is 07:50:00 for train 113 and 08:20:00 for train 111:

![](documentation/img/worked_example_earliest_entry.png)

Now, we just set the event times that result from propagating the _minimum_running_time_ along the path. We get:

![](documentation/img/worked_example_initial_assignment.png)

*************************************************************

![](documentation/img/worked_example_rule_violation.png)

*************************************************************

![](documentation/img/worked_example_better_assignment.png)