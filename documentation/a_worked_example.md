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

We notice train 111 must circulate sometime between 8:20, its earliest possible start time at its first _section_requirement_, and 8:50, its latest desired exit time at its last _section_requirement_. Train 111 also has a _section_requirement_ at some intermediate point 'B', where it wants to stop for a minimum of 3 minutes and exit that point no earlier than 8:30. Think of this as a commercial stop of the train. If the timetable says "Departure at 8:30", then the customers would be unhappy if it left at 8:25, or anytime before 8:30. Therefore, it makes sense to require a departure "no earlier than" 8:30. This is what the _exit_earliest_ for _section_requirement_ B ensures.

Likewise, train 113 must circulate sometime between 7:50 and 8:16 (so actually earlier than train 111). It has no other requirements.

Also note that, neither train specifies any connections that would have to be observed. All we have to worry about are the _earliest_ and _latest_ time requirements. That can't be too hard?

### Routes
We recall from the [short introduction](documentation/documentation#a-very-quick-introduction-to-our-timetabling-problem) that to producing a solution amounts to

* picking exactly one of the possible routes for each train, i.e. __selecting a path from a source to a sink node__ in the route graph
* then assign times to all events (nodes) on this path (such that all tweve [business rules](documentation/business_rules.md) are satisfied)

We also recall that the __route graphs are always directed and acyclic grpahs__.

So, what are the possible routes for the two services? We will see in the discussion of the [problem instance data model](documentation/input_data_model.md) how to derive the graph structure from the JSON. For the purpose of this example, let us just pretend we already knew that the two route graphs for service intentions 111 and 113 are actually identical and look as follows:

#### Route graphs for _service_intentions_ 111 and 113
_Hint:_ you may use the [route graph utility script](utils/route_graph.py) to produce the route graphs as a [networkx](https://networkx.github.io/) directed graph and that should produce the same graphs as in these pictures.

![](documentation/img/worked_example_route_graph.png)