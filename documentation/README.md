# Available Documentation
In this folder you should find all necessary background information to complete your task of producing a timetable to our problem instances.

What's available?:

* Before reading anything more detailed, we recommend to look at the [Very Quick Introduction](#a-very-quick-introduction-to-our-timetabling-problem) below. It gives a very brief, but surprisingly complete, description of what the problem is all about. <br>All the rest is basically just technicalities to make the data model and the rules precise.

* In [a worked example](documentation/a_worked_example.md) we solve a simple [sample problem instance](sample_files/sample_scenario.json) "on paper" from the ground up. <br>
This may also be helpful to work through before diving into the data model definitions below.

* The [input data model](documentation/input_data_model.md) describes the data model of the problem instances in detail.
* The [output data model](documentation/output_data_model.md) describes the data model in which the grader expects the solutions to the problem instances.

* The [business rules](documentation/business_rules.md) define the precise set of rules that have to be observed when producing a solution to a problem instance. It also describes how a solution is scored by the grader.


# A Very Quick Introduction to our Timetabling Problem

## The task at hand
Our task (or yours, if you are going to build a solver :wink:) is basically the following:

**Given**
* A list of trains to be scheduled, and
* For each train
    - a set of _Functional Requirements_, such as earliest departure time, latest arrival time, minimum stopping times, connections to other trains, etc.
    - a set (actually, a directed acyclic graph) of _routes_ it could take from origin to destination, together with minimum running times on the sections and a list of resources that are occupied while the train is in this section.

**Produce a timetable that**
-	does not violate any functional requirements
-	does not violate any physical requirements, such as minimum running time on a route section
-	does not result in resource occupation conflicts.

A **timetable** is an assignment of a (continuous) time instant to each event.

## What does it mean to 'not violate any functional/physical requirements'?
We have made precise what is considered a _valid_ (or _feasible_) solution through the definition of twelve individual rules. You will learn about them in the document [business rules](documentation/business_rules.md).

To give you a flavor of what these rules are like, here are two examples.

* [business rule #2](documentation/business_rules.md#concistency-rules) states that the solution must schedule each train in the problem instance. It is not allowed to ignore some of the trains.
* [business rule #104](documentation/business_rules.md#planning-rules) states that no two trains may occupy a common resource at any time

Basically, a solution must satisfy all twelve rules to be accepted. Actally, there is some leeway, because rule #101 may be bent a little bit, but don't worry about that for the time being.

## A note on the `routes`

A `route` actually consists of individual `route sections`. The sections attach to one another head-to-tail to form a directed acyclic graph (DAG). Each vertex in this DAG is called an `event`. It represents the event, when a train passes from one section to the next one._ We use the term `route graph` as a synonym for `route` in the following. A simple _route_ might look as follows - although realistic example have many more sections, typically between 50 and 100. 

![](documentation/img/route_graph_naked.png)

The graph encodes the set of **possible** paths the train can take. The train __must always starts on a source node__ (i.e. a node without incoming arcs) and __must always ends on a sink node__ (a node without outgoing arcs). In order to solve the timetabling problem, you must choose for each train exactly one such path through its route graph. Different paths usually occupy different resources. Also, some paths may be preferable to others; for example some sections may have a penalty associated if they are used. You will learn more about all this in the discussion of the [input data model](documentation/input_data_model.md) and the [objective function](documentation/business_rules.md#objective-function).