# sentinel-monitoring

Group Memebers : Brinda, Jui, Saurabh, Shradha

Architecture Diagram:
<img width="1038" alt="image" src="https://user-images.githubusercontent.com/22095857/168987779-a618d078-c4ae-4fb2-8bee-aa543a982720.png">

Failure Recovery:
<img width="1063" alt="Screen Shot 2022-05-18 at 12 53 48 AM" src="https://user-images.githubusercontent.com/22095857/168987865-dc05b4fb-6676-4f5a-93e2-2a8bec9360b7.png">


# How to run the code

To run the monitoring system, we need to follow the following steps. The bidirectional_multithread contains all the files:
* Monitor node and the nodes/clients should be up and running to check the demo with class integration
* For testing it on a single machine (test the monitoring separately), we need to change the master node ip and port to localhost:50051 for the master dummy node. Dummy nodes for testing individually are run on localhost:50071,72,73
* Run monitor node 1: python3 follower1.py
* Run monitor node 2: python3 follower2.py
* Run leader monitor node: python3 gang_leader.py
