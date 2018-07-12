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
* parameters

Let's go through them.

## label
This is just a human-readable identifier for the instance. It is of no concern otherwise.

## hash
A machine-readable identifier for the instance. This hash must be referenced when submitting a solution for this instance. See [Output Data Model](https://gitlab.crowdai.org/jordiju/train-schedule-optimisation-challenge-starter-kit/blob/master/data_model/output_data_model.md).

## parameters
Can be used to set global or solver-specific guidelines for the instance. Do not change these, as it would change the hash of the instance.

## service_intentions, or "funktionaleAngebotsbeschreibungen" in German
..._now it gets complicated_...

## routes, or "fahrwege" in German
..._and even more complicated_...