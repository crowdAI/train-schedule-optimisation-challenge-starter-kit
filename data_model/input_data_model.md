# Data Model of the Problem Instances

## Translation from and to German
Unfortunately, our data model was conceived in German. This cannot really be changed for this challenge, so it is what it is. In particular, the solutions your solver produces will also need to conform to the solution data model, which is also in German.

However: to help you work with English terminology internally, we provide translation helper scripts that you can use to translate a problem instance into English and to translate an English solution into the German terminology we require.

The translation script is [here](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/utils/translate.py).

## The data model
A _problem instance_, or a _scenario_ is a JSON file containing the following top-level elements:
* label
* hash
* service_intentions (funktionale Angebotsbeschreibungen)
* routes (fahrwege)
* ressourcen (resources)
* parameters

Let's go through them. You may use the small [sample scenario](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/sample_files/sample_scenario.json) as a concrete example.


## label
This is just a human-readable identifier for the instance. It is of no concern otherwise.

## hash
A machine-readable identifier for the instance. This hash must be referenced when submitting a solution for this instance. See [Output Data Model](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/data_model/output_data_model.md).

## parameters
Can be used to set global or solver-specific guidelines for the instance. Do not change these, as it would change the hash of the instance.

## service_intentions (funktionaleAngebotsbeschreibungen)
This is a list. Each item in the list is an individual _service_intention_. A _service_intention_ describes a specific train to be run. In particular, it specifies **all requirements** that the scheduler needs to observe when planning this particular train. These requirements can be of the following type:
* earliest allowed departure at certain points
* latest desired arrival at certain points
* commercial stops to be observed, including minimum stopping time at these stops
* connections to other trains (i.e. _service_intentions_), including minimum transfer time

### service intention (funktionaleAngebotsbeschreibungen)
An individual _service_intention_ consists of
* id: identifier for the train, or "service"
* route (fahrweg): a reference to the route graph, see below for details on the routes
* section_requirements (abschnittsvorgaben): a list of individual _section_requirements_. This is where the actual requirements for this train(service) are specified. Before we look at these, it is helpful to first discuss the model for the routes.


## routes (fahrwege)
Recall from the [Quick Introduction](data_model/quick_intro_scheduling.md) that a _route_ is modeled as a directed acyclic graph (DAG). It describes the possible ways for the train to move through the railway network. The nodes in the graph are the _events_ that occur along the way, such as "arrival at station X", "releasing resource Y", etc. For a directed arc we call the node at its tail the _entry event_ and the node at its head the _exit event_ from this arc.The directed arcs have associated to them a list of _resource occupations_ (ressourcenbelegungen). These are the resources that a train on this route will occupy, while it is traveling on this arc, i.e. in the timespan between the entry event and the exit event. Each arc also has a minimum running time, which gives the _minimum_ duration between entry and exit event. There is no maximum duration, by the way. A train may spend as much time on a section as it likes. Of course, it keeps using the resources of this route section during this time.

A specialty of route graph are the _section markers_ that may be associated to certain arcs (route sections). These provide the link to the section requirements in the service intentions. We will discuss these below.

The following image illustrates a typical route DAG. It represents route XYZ (_**ToDo: modify sample scenario so it fits with the picture**_) in the [sample scenario](sample_files/sample_scenario.json). The red labels denote the resource occupations of each route section. The blue labels denote the section markers, which are typically not present on every section.

_**ToDo: insert proper image**_
![](data_model/img/img.png)

Modeling a graph in a JSON structure in a human-readabl way is not exactly a joy. We have taken the approach that paths in a graph can be grouped into so-called _route paths_. Where these route paths join or fork is governed by _route alternative marker labels_ of individual route sections. In the following image, the route paths are highlighted.

_Note: There are many ways to cut the graph into segments of linear paths. In the end, all that matters is the resulting DAG. The route paths are only an aid for a human editing the file manually._

_**ToDo: insert proper image**_
![](data_model/img/img.png)


_**ToDo: describe the formal model**_

### section requirement (abschnittsvorgabe)
With the understanding of the routes, the meaning of the _section requirements_ in a service intention is now easily understood.

Each section requirement references a _section_marker_. This means that "this requirement is meant for a route section that carries this label as a _section_marker_". The section requirement can ask:
* that a certain time window be respected for the entry event by setting entry_earliest (einMin) and/or entry_latest (einMax) accordingly
* same thing for the exit event by setting exit_earliest (ausMin) and/or exit_latest (ausMax)
* a minimum stopping time be observed on this route section by setting min_stopping_time (minHaltezeit). This stopping time will be _in addition_ to the minimum_running_time
* the connections to other trains (service intentions) to be observed

Also, the requirement can specify relative factors _entry_delay_weight_ (einVerspaetungsfaktor) and _exit_delay_weight_ (ausVerspaetungsfaktor). These weights are used in the calculation of the [objective function](data_model/objective_function.md).

Finally, section requirements have a _sequence_number_. They must be fulfilled in the order given by the sequence number. You do not need to worry about this. The route graphs provided are always such that it is _impossible_ to fulfil them in any other order (remember the route graph is acyclic). So the sequence field is not important for you as a solver.

Summarizing: The formal model for a _section_requirement_ is as follows

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| sequence_number (reihenfolge)                                                                 | integer                           | see text above    |
| type (typ)                                                                                    | text                              | a text field describing what this requirement is meant to represent. Has no effect on processing. You may ignore it.   |
| minimum_stopping_t    ime (minHaltezeit)                                                      | ISO duration                      |  see text above |
| entry_earliest (einMin) and/or entry_latest (einMax)                                          | HH:MM[:SS] formatted time-of-day  |  see text above |
| exit_earliest (ausMin) and/or exit_latest (ausMax)                                            | HH:MM[:SS] formatted time-of-day  |  see text above |
| entry_delay_weight (einVerspaetungsfaktor) and _exit_delay_weight_ (ausVerspaetungsfaktor)    | non-negative float                |  used to calculate total delay penalties in the [objective function](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/planning_rules/planning_rules.md#ojective-function) |
| connections (anschluesse)                                                                     | list of connections, see below    |  see below |

#### connections (anschluesse)
Connections are directed. They point _from_ a train that gives a connection _to_ another train that accepts the connection. In our model, a connection is listed under the train that _gives_ it.

The model is as follows:

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| min_connection_time (minAnschlusszeit)                                                        | ISO duration                      | minimum duration required between arrival and departure event. See [Planning Rules](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/planning_rules/planning_rules.md) for details.    |
| id                                                                                            | text                              | technical id. Irrelevant during processing |
| onto_service_intention (aufZugfahrt)                                                          | text                              | reference to the _service_intention_ that accepts the connection|
| onto_section_marker (aufAbschnittskennzeichen)                                                | text                              | reference to a section marker. Specifies which route_sections in the _onto_service_intention_ are candidates to fulfil the connection|



