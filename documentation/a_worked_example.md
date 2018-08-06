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

*******************
![](documentation/img/worked_example_selected_routes.png)
*******************

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

******************
![](documentation/img/worked_example_minimum_running_time_and_section_markers.png)
******************

Now the earliest possible starting times for the trains are given by the _entry_earliest_ time of the first _section_requirement_ (by the way: it is a general convention of all problem instances, that the first _setion_requirement_ always has an _entry_earliest_, and the last _section_requirement_ always has an _exit_latest_)

In our case, this is 07:50:00 for train 113 and 08:20:00 for train 111:

******************
![](documentation/img/worked_example_earliest_entry.png)
******************

Now, we just set the event times that result from propagating the _minimum_running_time_ along the path. We get:

******************
![](documentation/img/worked_example_initial_assignment.png)
******************

This is our initial solution. Let's bring it into the shape of the [solution data model](documentation/output_data_model.md). For this, we put the _train_run_sections_ (the arcs in the picture above) in a list and fill in their information. Also, we must add the reference to the problem instance so the grader will know to what problem this is supposed to be a solution. You can download the resulting solution file [here](sample_files/sample_scenario_solution_initial_times.json). It looks like this:

******************
![](documentation/img/worked_example_initial_assignment_solution.png)
******************


### 3. Check Business Rules
We check if we have produced a feasible solution, i.e. whether it satisfies all [business rules](documentation/business_rules.md).

We check the [Consistency Rules](documentation/business_rules.md#concistency-rules) first

* #1 problem_instance_hash present: Yes, the _hash_ -1254734547 of the [sample instance](sample_files/sample_scenario.json) is correctly entered as the _problem_instance_hash_ :heavy_check_mark:
* #2 each train is scheduled: We schedule both trains 111 and 113. :heavy_check_mark:
* #3 ordered _train_run_sections_: Yes, we simply numbered their _sequence_numbers_ incrementally from 1 to 7. :heavy_check_mark:
* #4 reference valid route: Yes, we have added all the necessary information. :heavy_check_mark: <br>Recall (see [here](documentation/output_data_model.md#train_run_section)) that the _route_section_id_ is constructed from the pattern _route_._id_#_route_section_._sequence_number_. <br>Also note that train 111 uses one _route_section_ from the _route_path_ with _id_ 3, while train 113 only uses _route_sections_ from _route_path_ 1.
* #5 train_run_sections form a path in the route graph: Yes, they do, we chose them exactly like that [above](#1-select-a-route). :heavy_check_mark:
* #6 pass through all section_requirements: Yes, train 111 passes A, B and C, train 113 passes A and C, as required. :heavy_check_mark: <br>__Important remark:__ In fact, we guarantee that if you pick __any__ path from a source to a sink node in the route graph of a _service_intention_ you will pass all required _section_markers_ __and__ do so in the correct order. All you need to do, therefore, is make sure you add that information to the _train_run_sections_ in their _section_requirement_ field.
* #7 consistent entry_time and exit_time times: Yes, by construction we just repeat the _exit_time_ of a _train_run_section_ as the _entry_time_ of the next one ('next' according to their _sequence_number_). :heavy_check_mark:

Let's check the [Planning Rules](documentation/business_rules.md#planning-rules) next

* #101 Time windows for _latest_-requirements: We have two _latest_ requirements (see the [file](sample_files/sample_scenario.json) or screenshot [above](#service-intentions):
    - _exit_latest_ of 08:16:00 for _service_intenation_ 113 in C. The _train_run_section_ associated to _section_requirement_ C has an _exit_time_ of 07:54:05, which is certainly before 8:16 :heavy_check_mark:
    - _exit_latest_ of 08:50:00 for _service_intention_ 111 in C. Here, the relevant _train_run_section_ has _exit_time_ 08:24:05 :heavy_check_mark:

* #102 Time windows for _earliest_-requirements: We have three _earliest_requirements:
    - _service_intention_ 113: 
        - _entry_earliest_ 07:50:00 for section A. We scheduled this event for exactly this time, which is ok. :heavy_check_mark:
    - _service_intention_ 111:
        - _entry_earliest_ 08:20:00 for section A. We scheduled this event for exactly this time. :heavy_check_mark:
        - _exit_earliest_ 08:30:00 for section B. We scheduled this event for 08:21:57. :x:

*************************************************************
![](documentation/img/worked_example_rule_violation.png)
*************************************************************

We have found a rule violation. Let's fix that.

### Fix event times and try again

In order to satisfy the "_exit_earliest_ at 8:30" requirement for 111 in B and stay true to our idea of scheduling each event as early as possible, we just postpone that event from 08:21:57 to 08:30:00 and propagate the times for the events following it. We get get following picture (adjusted event times in red):

*************************************************************
![](documentation/img/worked_example_better_assignment.png)
*************************************************************
<br><br>
__Check Business Rules again__

It is immediately obvious that the changes we made do not influence the Consistency Rules #1 - #7. We don't check them in detail anymore. 

__[Planning Rules](documentation/business_rules.md#planning-rules):__

* #101 Time windows for _latest_-requirements: We didn't change anything for train 113, just check 111 again.
    - _exit_latest_ of 08:50:00 for _service_intention_ 111 in C. We have postponed this event from 08:24:05 to 08:32:08, but that is still well before the deadline. :heavy_check_mark:

* #102 Time windows for _earliest_-requirements: Again, train 113 remains unchanged and was ok before. Just check 111 again. <br>We have two _earlieste_requirements for train 111:
    - _entry_earliest_ 08:20:00 for section A. Event is still scheduled at 08:20:00. :heavy_check_mark: 
    - _exit_earliest_ 08:30:00 for section B. __Event is now scheduled at exactly 08:30:00.__ :heavy_check_mark:

* #103 Minimum section time: Exactly by construction, we always spend at least the _minimum_running_time_ on each section. In order to satisfy this rule, we just have to check if, for some _train_run_section_, we also need to account for a _min_stopping_time_ associated with that section. <br>In our _service_intentions_ (see screenshot [above](#service-intentions)), we have only one _section_requirement_ that requires a stopping time, namely _section_requirement_ #2 for train 111, which refers to the section 'B' and requires 3 minutes of stopping time.

The _train_run_section_ for 'B' has an _entry_time_ of 08:21:25 and an _exit_time_ of 08:30:00. We have _exit_time_ - _entry_time_ = 8 minutes and 35 seconds.

The rule says that 8 minutes and 35 seconds must be greater-or-equal to the _minimum_running_time_ __plus__ the _min_stopping_time_. But the latter two only sum to 3 minutes and 32 seconds. So the condition of the rule is satisfied :heavy_check_mark:

* #104 Resource Occupations: We must check that the two trains do not try to occupy two resources "at the same time" (in fact, there must be a positive separation between resource occupations given by the release time of the resource, typically ~30s). <br><br>__This rule is what makes the problem NP-complete__. In our case, we are lucky, because there are only two trains. They actually _do_ use common resources (which resource occupations are occupied on which sections is illustrated in the route graph [above](#route-graphs-for-service_intentions-111-and-113)). However, we note that 

    - train 113 ends at 07:54:05
    - train 111 starts at 08:20:00
    - all resources in the [instance](sample_files/sample_scenario.json) have a _release_time_ of 30s

In other words, __after 07:54:35 train 113 will certainly not occupy any resources anymore at all__, train 111 will therefore never come into conflict. The rule is satisfied. :heavy_check_mark:

* #105 Connections: There are no connections defined in our two _service_intentions_, there is nothing to check. :heavy_check_mark:

We have produced a feasible solution. It is actually even an _optimal_ solution, meaning it receives an [objective value](documentation/business_rules.md#objective-function/busine) of 0. Here it is again all its glory (you can download the solution file [here](sample_files/sample_scenario_solution.json)).

*************************************************************
![](documentation/img/worked_example_final_solution.png)
*************************************************************
