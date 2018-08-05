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

### Routes
What are the possible routes for the two services? As mentioned in the [short introduction](documentation/documentation#a-very-quick-introduction-to-our-timetabling-problem), the possible routes are modeled as a directed acyclic graph. We will see in the discussion of the [problem instance data model](documentation/input_data_model.md) how to derive the graph structure from the JSON. For the purpose of this example, let us just assume that somebody told us that the two route graphs for service intentions 111 and 113 are acutally identical and look as follows: <br>_Hint:_ you may use the [route graph utility script](utils/route_graph.py) to produce the route graphs as a [networkx](https://networkx.github.io/) directed graph and that should produce the same graphs as in these pictures.

#### Route graphs for _service_intentions_ 111 and 113
![](documentation/img/worked_example_route_graph.png)