# Starter-kit Repo for the [SBB Train Schedule Optimisation Challenge](https://www.crowdai.org/challenges/train-schedule-optimisation-challenge) on [crowdAI](https://www.crowdai.org)

In this repo you will find background material, sample files and support scripts that help you to get started with the challenge.

## How to get started?

This challenge requires a bit of explanation before you can get started. While the general idea is quite simple, and there are only a grand total of twelve rules that need to be taken into account when producing a timetable, the data models used require an introduction.

We recommend that you proceed through the documentation in the following order:

1. First, read the [Quick Introduction to the Timetabling Problem](documentation/quick_introduction.md). After this, you should be able to relate to the problem and start to get a feeling for the algorithmic difficulties involved.
2. Second, it is probably a good idea to go through the [Worked Example](documentation/a_worked_example.md). In that document, we take a very simple sample problem, produce a solution from the ground up (in the required solution data format) and then verify that we indeed satisfy all twelve timetabling rules.
3. After the first two, you may proceed with the further documentation (see [below](#what-can-i-find-in-this-repo)), and maybe start to solve the simple instances in parallel with learning the fine details of the data models and the timetabling rules.
4. Once you really want to start solving the instances, you should also check out the [description of the instances](documentation/instance_description.md) and [what to submit](documentation/what_to_submit.md). The first document gives you an idea about the size (and difficulty) of the problem instances, the second walks you through a sample submission.<br><br>In general, you should start solving the simple instances first. More information on that in the [description of the instances](documentation/instance_description.md).

## What do I have to do?
You must try to generate solutions to the nine problem instances in [this folder](problem_instances).

Once you have solutions, you can submit them through the [Challenge page on crowdAI](https://www.crowdai.org/challenges/train-schedule-optimisation-challenge/submissions). 

In order to submit, it is __not necessary to solve all nine problem instances__. You can also submit an arbitrary subset of them. However, each missing solution will incur a penalty of 10'000 points. As soon as you manage to find a solution with an objective value better (i.e. lower) than 10'000, you should therefore include that solution in the submission.

By the way, we provide [sample solutions](problem_instances/sample_solutions) to seven of the nine problem instances. These seven solutions are also available as a [sample submission](problem_instances/sample_solutions/sample_submission.json). You may use these solutions to test the submission workflow and verify the data models. You must not use them as a basis for your solver, however, see the according [challenge rules](https://www.crowdai.org/challenges/train-schedule-optimisation-challenge).

The goal is to create a submission with __as small a score as possible__.

## What can I find in this Repo?

* In the [Documentation](documentation) folder you find all documentation texts, such as
    - the [Quick Introduction](documentation/quick_introduction.md) mentioned above
    - the [Worked Example](documentation/worked_example.md)
    - description of the [input data model](documentation/input_data_model.md)
    - description of the [output data model](documentation/output_data_mode.md)
    - definition of the twelve 'timetabling', or [business rules](documentation/business_rules.md)
    - A [description](documentation/instance_description.md) of the nine problem instances that make up the challenge

* The [sample_files](sample_files) folder contains some simple sample instances and solution. We use these in the documentation to explain our data models and the grading function.

* The [problem_instances](problem_instances) folder contains the actual timetabling problem instances that you need to solve for this challenge. Also, you find in a subfolder sample solutions (although not very good ones) to some of the instances and a sample submission.

* The [utils](utils) folder contains some utilities such as
    - a [script](utils/validate_solution.py) to evaluate _individual_ solutions to problem instances without a "formal" submission. This is very helpful when trying to tune your algorithms. There is also an accompanying [notebook](utils/validate_solution.ipynb) explaining its use. 
    - a [script](utils/route_graph.py) that transforms the routes in a problem instance into directed graphs in the [networkx](https://networkx.github.io/) package. You may find this useful when trying to work with the route graph algorithmically in your solver, or just for visualization purposes.