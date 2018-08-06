# Description of the Problem Instances

Not part of the 'competition' is the [sample instance](sample_files/sample_scenario.json). It is the simplest instance of all and you should start your solving adventures with this one. 

## The official nine  [Problem Instances](problem_instances)

As a general rule of thumb, the complexity of the instances increases according to their prefix-number. 01 is clearly the simplest one, 09 is clearly the hardest one. Between 05 and 08, one cannot really make a general statement. For some algorithms, an instance may be very easy, while for others the same one may be hard but a different one more suitable. Just give it a go and find out!

__A note on solvability:__ All instances except 05 are solvable with objective value 0, i.e. satisfying all [business rules](documentation/business_rules.md) and avoiding routes with _penalty_. Strictly speaking, we are not entirely sure for instance 09, because our benchmark solvers have not been able to solve that instance. But we strongly expect that is the case. 

| Instance          | Description       |
| -------------     |-------------      |
| [01_dummy](problem_instances/01_dummy.json)   | Very simple instance. Having solved the sample instance above, you should solve this one <br>- 4 trains<br>- minimal routing alternatives<br>- no connections                         |
| [02_a_little_less_dummy](problem_instances/02_a_little_less_dummy.json)   | Still simple. More trains than 01, but still very minimal routing possibilities. Actually, most trains have a fixed route (i.e. the route graph is just a linar path) <br>- 58 trains<br>- minimal routing alternatives<br>- no connections                         |
| [03_FWA_0.125](problem_instances/03_FWA_0.125.json)   | Getting more difficult. More trains than 02, but still quite limited routing possibilities. First instance with connections, so you must implement the logic to conform to the [Connections Business Rule #105](documentation/business_rules.md)  <br>- 143 trains<br>- minimal routing alternatives<br>- first instance with connections     |
| [04_V1.02_FWA_without_obstruction](problem_instances/04_V1.02_FWA_without_obstruction.json)   | Similar to 03. A few more trains.  <br>- 148 trains<br>- few routing alternatives     |
| [05_V1.02_FWA_with_obstruction](problem_instances/05_V1.02_FWA_with_obstruction.json)   | __This instance cannot be solved with objective value 0!__ In other words, it is impossible to satisfy all twelve [business rules](documentation/business_rules.md). Since rule #101 is the only one that can be 'bent', you must try to find a solution that __minimizes__ the delay. The sample solutin for this instance is far from optimal. <br>For most solvers, this instance is far harder than 04, even though it only contains one _service_intention_ more and is otherwise identical.  <br>- 149 trains<br>- few routing alternatives <br>- typically difficult to solve optimally     |
| [06_V1.20_FWA](problem_instances/06_V1.20_FWA.json)   | One of the larger instances, many trains and for many of them a large number of routing alternatives   <br>- 365 trains<br>- quite some routing alternatives |
| [07_V1.22_FWA](problem_instances/07_V1.22_FWA.json)   | Similar to 06, but roughly 100 trains more  <br>- 467 trains<br>- quite some routing alternatives |
| [08_V1.30_FWA](problem_instances/08_V1.30_FWA.json)   | Next to instance 09, this is the instance with the most routing alternatives. However, it contains a lot fewer trains than 06 and 07. <br>We do not provide a sample solution for this instance.  <br>- 133 trains<br>- lots of routing alternatives |
| [09_ZUE-ZG-CH_0600-1200](problem_instances/09_ZUE-ZG-CH_0600-1200.json)   | All in all the largest instance. Contains 'only' 287 trains, but each of them has large amount of possible routings.<br>We do not provide a sample solution for this instance. It is probably solvable with objective value 0, although we have not been able to find such a solution so far. <br>- 287 trains<br>- lots of routing alternatives |


# In what order should I solve them?

You should probably
* start with the (almost trivial) [sample instance](sample_files/sample_scenario.json) just to get the technicalities and the data models right
* then proceed to the simplest official problem instances [01](problem_instances/01_dummy.json) and [02](problem_instances/02_a_little_less_dummy.json) 
* once solved, proceed to the remaining instances. The remaining ones also feature connections, you can solve the previous ones without worrying about those.

# Happy Solving!