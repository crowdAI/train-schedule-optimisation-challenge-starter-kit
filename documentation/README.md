# Available Documentation
In this folder you should find all necessary background information to complete your task of producing a timetable to our problem instances.

Specifically:

* The document [input data model](documentation/input_data_model.md) describes the data model of the problem instances in detail.
* The document [output data model](documentation/output_data_model.md) describes the data model in which the grader expects the solutions to the problem instances.
* The document [business rules](documentation/business_rules.md) defines the set of rules that have to be observed when producing a solution to a problem instance. It also describes how a solution is scored by the grader.

These documents are rather detailed, and it is easy to lose sight of the forest for the trees. For this reason, we advise to first read the following "Very Quick Introduction".

# A Very Quick Introduction to our Timetabling Problem

Our task (or yours, if you are going to build a solver :wink:) is basically the following:

Given 
* A list of trains to be scheduled, and
* For each train
    - a set of _Functional Requirements_, such as earliest departure time, latest arrival time, minimum stopping times, connections to other trains, etc.
    - a set (actually, a directed acyclic graph) of _routes_ it could take from origin to destination, together with minimum running times on the sections and a list of resources that are occupied while the train is in this section.

Produce a timetable that
-	does not violate any Functional Requirements
-	does not violate any physical constraints, such as minimum running time on a route section
-	does not result in resource occupation conflicts.

A **timetable** is an assignment of a (continuous) time instant to each event.

_Note: A route actually consists of individual **route sections**. The sections attach to one another head-to-tail to form a DAG. Each vertex in this DAG is called an **event**. It represents the event, when a train passes from one section to the next one._