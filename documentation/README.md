# Available Documentation
In this folder you should find all necessary background information to complete your task of producing a timetable to our problem instances.

What's available?:

* Before reading anything more detailed, we recommend to look at the [Very Quick Introduction](#a-very-quick-introduction-to-our-timetabling-problem) below. It gives a very brief, but surprisingly complete, description of what the problem is all about. <br>All the rest is basically just technicalities to make the data model and the rules precise.

* In [a worked example](documentation/a_worked_example.md) we solve a simple [sample problem instance](smaple_files/sample_scenario.json) "on paper". <br>
This may also be helpful to work through before diving into the data model definitions below.

* The [input data model](documentation/input_data_model.md) describes the data model of the problem instances in detail.
* The [output data model](documentation/output_data_model.md) describes the data model in which the grader expects the solutions to the problem instances.

* The [business rules](documentation/business_rules.md) define the precise set of rules that have to be observed when producing a solution to a problem instance. It also describes how a solution is scored by the grader.


# A Very Quick Introduction to our Timetabling Problem

Our task (or yours, if you are going to build a solver :wink:) is basically the following:

Given 
* A list of trains to be scheduled, and
* For each train
    - a set of _Functional Requirements_, such as earliest departure time, latest arrival time, minimum stopping times, connections to other trains, etc.
    - a set (actually, a directed acyclic graph) of _routes_ it could take from origin to destination, together with minimum running times on the sections and a list of resources that are occupied while the train is in this section.

Produce a timetable that
-	does not violate any Functional Requirements
-	does not violate any physical requirements, such as minimum running time on a route section
-	does not result in resource occupation conflicts.

A **timetable** is an assignment of a (continuous) time instant to each event.

_Note: A route actually consists of individual **route sections**. The sections attach to one another head-to-tail to form a DAG. Each vertex in this DAG is called an **event**. It represents the event, when a train passes from one section to the next one._