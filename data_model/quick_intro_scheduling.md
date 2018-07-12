# A very quick Introduction to our Scheduling Problem

Our task (or yours, if you are going to build a solver ;)) is basically the following:

Given 
* A list of trains to be scheduled, and
* For each train
    - a set of Functional Requirements, such as earliest departure time, latest arrival time, minimum stopping times, connections to other trains, etc.
    - a set (actually, a directed acyclic graph) of routes it could take from origin to des-tination, together with minimum running times on the sections and which re-sources are occupied while the train is this section.

Produce a schedule that
-	does not violate any Functional Requirements
-	does not violate any physical constraints, such as minimum running time on a route sec-tion
-	does not result in resource occupation conflicts.

A **schedule** is an assignment of a (continuous) time instant to each event.

_Note: A route actually consists of individual **route sections**. The sections attach to one another head-to-tail to form a DAG. Each vertex in this DAG is called an **event**. It rep-resents the event, when a train passes from one section to the next one._

