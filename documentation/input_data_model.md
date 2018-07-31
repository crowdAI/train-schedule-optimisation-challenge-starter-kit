# Input Data Model
This document describes the data model for the [problem instances](problem_instances).

## A Note on translation from and to German
Unfortunately, our data model was conceived in German. This cannot really be changed for this challenge. It is what it is. In particular, the solutions your solver produces will also need to conform to the [solution data model](documentation/output_data_model.md), which is also in German.

However: If you prefer to work with English terminology internally, we provide translation helper scripts that you can use to translate a problem instance into English and to translate an English solution into the German terminology we require. The translation script is [here](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/utils/translate.py).

## Data Model of the Problem Instances

A _problem instance_, or a _scenario_, is a JSON file containing the following top-level elements:
* label
* hash
* service_intentions (a fancy name for 'train including all its requirements')
* routes
* resources
* parameters

Let's go through them. You may use the small [sample scenario](sample_files/sample_scenario_simple.json) as a concrete example. This looks like this: It contains 9 trains to be scheduled, 2 routes, and 33 resources.

![](documentation/img/scenario_top_level.png)


### label
This is just a human-readable identifier for the instance. It is of no concern otherwise.

### hash
A machine-readable identifier for the instance. This hash must be referenced when submitting a solution for this instance. See [Output Data Model](documentation/output_data_model.md#problem_instance_hash-verkehrsplanhash).

### service_intentions
This is a list. Each item in the list is an individual _service_intention_. In the [example](sample_files/sample_scenario_simple.json), it looks like this:

![](documentation/img/service_intentions.png)

It describes a specific train to be run. In particular, it specifies which _route_ a train can take (see below) and **all requirements** that the scheduler needs to observe when planning this particular train. For this challenge, only a very limited set of four types of such requirements need to be considered. We define them below in the [section_requirement](#section-requirement).

#### service intention
An individual _service_intention_ looks like this:

![](documentation/img/service_intention.png)

It consists of
* id: identifier for the train, or "service"
* route: a reference to the route graph, see [below](#routes) for details on the routes
* section_requirements: a list of individual _section_requirements_. This is where the actual requirements for this train(service) are specified. Before we look at these (subsection [section_requirements](#section-requirement) below), it is helpful to first discuss the model for the _routes_.

### routes
Recall from the [Quick Introduction](documentation/README.md#a-very-quick-introduction-to-our-timetabling-problem) that a _route_ is modeled as a directed acyclic graph (DAG). It describes the possible ways for the train to move through the railway network. The nodes in the graph are the _events_ that occur along the way, such as "arrival at station X", "releasing resource Y", etc. A directed arc in the route graph is called a _route_section_. For a route_section, we call the node at its tail the _entry event_ and the node at its head the _exit event_ from this route_section. The route_sections have associated with them a list of _resource occupations_. These are the resources that a train on this route will occupy, while it is traveling on this arc, i.e. in the timespan between the entry event and the exit event. Each arc also has a minimum running time, which gives the _minimum_ duration between entry and exit event. There is no maximum duration, by the way. A train may spend as much time on a section as it likes. Of course, it keeps using the resources of this route section during this time.

As an example, we look at the [sample scenario with routing alternatives](sample_files/sample_scenario_with_routing_alternatives.json). The following images illustrate _route_1_ in that scenario:

![](documentation/img/route_sample.png)

The DAG for _route_1_ looks as follows: Nodes are the _events_ and arcs are the individual _route_sections_. The red labels are _route_alternative_markers_ (see the explanation on _route paths_ just below), the black labels are the _sequence_number_ of the individual _route_section_. 

![](documentation/img/route_graph_with_legend.png)

A specialty of route graph are the _section markers_ that may be associated to certain arcs (_route_section_). These provide the link to the section requirements in the service intentions. We will discuss them in more detail below. In this sample DAG, there are the following _section_markers_ (in blue):

![](documentation/img/route_DAG_section_markers.png)

Modeling a graph in a JSON structure in a human-readabl way is not exactly a joy. We have taken the approach that paths in a graph can be grouped into so-called _route paths_. These are paths (i.e. linear subgraphs) in the route graph. Distinct _route_paths_ can be "glued" together at events that share the same _route alternative marker labels_. In the following image, the individual _route_paths_ are encircled for clarity. Again, the red labels are the _route alternative marker labels_.

_Note: There are many ways to cut the graph into segments of linear paths. In the end, all that matters is the resulting DAG. The route paths are only an aid for a human editing the file manually._

![](documentation/img/route_DAG_route_paths.png)

In the formal data model, a _route_ has
* an id
* a list of _route_paths_, which themselves are a list of _route_sections_. These are the ineresting objects. They are built as follows

#### _route_section_ (fahrwegabschnitt):

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| sequence_number (reihenfolge)                                                                 | integer                           | an ordering number. The train passes over the route_sections in this order. This is necessary because the JSON specification does not guarantee that the sequence in the file is preserved when deserializing.   |
| penalty                                                                                       | non-negative float                | used in the [objective function](documentation/business_rules.md#objective-function) for the timetable. If a train uses this route_section, this penalty accrues. <br> This field is optional. If it is not present, this is equivalent to penalty = 0.     |
|  route_alternative_marker_at_entry (vonVerzweigungen)                                         | text                              | a label for the _entry event_ into this route_section. Route sections from other _route_paths_ with the same label are "glued" together, i.e. become the same node in the route graph. |
|  route_alternative_marker_at_exit (nachVerzweigungen)                                         | text                              | dito for the _exit event_ from this route_section    |
| _starting_point_ and _ending_point_ (startpunkt and endpunkt)                                 | text                              | used in visualisations of the timetable. It has no meaning otherwise. But note that each route_section begins where the last one ends, which, if you think about it, kinda makes sense :wink:    |
|   minimum_running_time (minFahrzeit)                                                          | ISO duration                      | minimum time (duration) the train must spend on this _route_section_|
|   resource_occupations (ressourcenbelegungen)                                                 | List of _resource_occupation_s    | see [below](#resource_occupation-ressourcenbelegung)|
|   section_markers (abschnittskennzeichen)                                                     | List of text                      | labels that mark this _route_section_ as a potential section to fulfil a _section_requirement_ that has any of these as _section_marker_. <br>_Note_: In all our problem instances, each _route_section_ has at most one _section_marker_, i.e. the list has length at most one. |

#### _resource_occupation_ (ressourcenbelegung):

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| resource (ressource)                                                     | text                           | a reference to the id of the resource that is occupied |
| occupation_direction (belegungsrichtung)                                 | text                           | a description of the direction in which the resource is occupied. This field is only relevant for resources that allow "following" trains. See the description of resources [below](#resources-ressourcen). |

#### section requirement (abschnittsvorgabe) [element of a [service_intention](#service-intention-funktionaleangebotsbeschreibung)]
With the understanding of the routes, the meaning of the _section requirements_ in a service intention now makes more sense.

Each section_requirement references a _section_marker_. This means that "this requirement can be satisfied on any route_section that carries this label as a _section_marker_". The section requirement can ask:
* that a certain time window be respected for the entry event by setting entry_earliest (einMin) and/or entry_latest (einMax) accordingly
* same thing for the exit event by setting exit_earliest (ausMin) and/or exit_latest (ausMax)
* a minimum stopping time be observed on this route section by setting min_stopping_time (minHaltezeit). This stopping time will be _in addition_ to the minimum_running_time
* the connections to other trains (service intentions) to be observed

Also, the requirement can specify relative factors _entry_delay_weight_ (einVerspaetungsfaktor) and _exit_delay_weight_ (ausVerspaetungsfaktor). These weights are used in the calculation of the [objective function](documentation/business_rules.md#objective-function).

Finally, section_requirements have a _sequence_number_. The requirements must be fulfilled in the order given by the sequence number. For example, if section_requirement with sequence_number 1 encodes the information for a "commercial stop in Berne" and the requirement with sequence_number 2 the information for a "commercial stop in Zurich", then it is not allowed to schedule the stop in Zurich before the one in Berne. In principle, this could make things very complicated. However, __you do not need to worry about this__. We make sure that the route graphs in the problem instances are always such that it is _impossible_ to fulfil the section_requirements in any other order (remember the route graph is a DAG!). So __the sequence field is not important for you as a solver.__

Summarizing: The formal model for a _section_requirement_ is as follows

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| sequence_number (reihenfolge)                                                                 | integer                           | see text above. Also needed because JSON deserialization may not preserve order    |
| type (typ)                                                                                    | text                              | a text field describing what this requirement is meant to represent, such as start of a train, a scheduled stop, etc. Has no effect on processing. You may ignore it.   |
| minimum_stopping_time (minHaltezeit)                                                      | ISO duration                      |  see text above |
| entry_earliest (einMin) and/or entry_latest (einMax)                                          | HH:MM[:SS] formatted time-of-day  |  see text above |
| exit_earliest (ausMin) and/or exit_latest (ausMax)                                            | HH:MM[:SS] formatted time-of-day  |  see text above |
| entry_delay_weight (einVerspaetungsfaktor) and _exit_delay_weight_ (ausVerspaetungsfaktor)    | non-negative float                |  used to calculate total delay penalties in the [objective function](documentation/business_rules.md#objective-function) |
| connections (anschluesse)                                                                     | list of connections, see below    |  see below |

#### connections (anschluesse)
Connections are directed. They point _from_ a train that gives a connection _to_ another train that accepts the connection. In our model, a connection is listed under the train that _gives_ it.

The model is as follows:

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| min_connection_time (minAnschlusszeit)                                                        | ISO duration                      | minimum duration required between arrival and departure event. See [Business Rules](documentation/business_rules.md) for details.    |
| id                                                                                            | text                              | technical id. Irrelevant during processing |
| onto_service_intention (aufZugfahrt)                                                          | text                              | reference to the _service_intention_ that accepts the connection|
| onto_section_marker (aufAbschnittskennzeichen)                                                | text                              | reference to a section marker. Specifies which route_sections in the _onto_service_intention_ are candidates to fulfil the connection|

### resources (ressourcen)

Resources are used to model which parts of the track infrastructure are used by a train while on a certain _route_section_ . A resource that is used is modeled as a _resource_occupation_ on the _route_section_, see above. Resource occupations always begin at the _entry_ into a _route_section_ and end at the _exit_ from a _route_section_. Typically, this is not the same route_section. Rather, a resource is usually occupied over several continuous route_sections.

In general, we use two kinds of resources to model different behaviour and level-of-detail:

* _blocking_ resources which means they must be released by a train before another train can start occupying them
* _following_ resources, which allow two trains to occupy them concurrently, as long as
    - they are separated at entry and exit by at least the _following_separation_
    - the order of the trains is the same at entry and exit, i.e. they do not overtake each other while using this resource.

**However, in the problem instances provided for this Challenge, you will only find resources of _blocking_ type. To participate in this challenge, it is therefore sufficient for you to consider only blocking logic.**

The model for a _resource_ is as follows:

| Field                                                                                         | Format                            | Description    |
| -------------     |-------------      | -----         |
| id                                                        | text                      | unique identifier for the resource. This is referenced in the _resource_occupations_    |
| release_time (freigabezeit)                               | ISO duration              | describes how much time must pass between release of a resource by one train and the following occupation by the next train. See [Business Rules](documentation/business_rules.md) for details.  |
|  following_allowed (zugfolgeErlaubt)                      | bool                      | flag whether the resource is of _following_ type (true) or of _blocking_ type (false). <br> As mentioned, __all resources in all the provided problem instances have this field set to__ _false_|

### parameters
Can be used to set global or solver-specific guidelines for the instance. Do not change these, as it would change the hash of the instance.