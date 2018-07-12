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

The following image illustrates a typical route DAG. The red labels denote the resource occupations of each route section. The blue labels denote the section markers, which are typically not present on every section.

![](data_model/img/img.png)
..._and even more complicated_...



### section requirement (abschnittsvorgabe)
This is where the actual requirements are specified. In order to understand what these mean, it is helpful to think of a train (service intention) as a sequence of _events_. 



