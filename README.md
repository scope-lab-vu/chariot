[![Build Status](https://travis-ci.org/visor-vu/chariot.svg?branch=master)](https://travis-ci.org/visor-vu/chariot)

# CHARIOT

## Summary
CHARIOT is a holistic solution that facilitates design, development, and management of distributed systems. Although the current implementation of CHARIOT was designed and tested with use-case scenarios specific to the domain of [extensible Cyber-Physical Systems(CPS)](http://etd.library.vbe.proxy.library.vanderbilt.edu/available/etd-11172016-154749/unrestricted/Pradhan.pdf), the underlying concepts are applicable to distributed systems in general. Following are the key aspects of CHARIOT:
* Design-time, generic system description using follwoing abstract concepts: 
   * The goal/mission of a system and ojectives required to achieve a system's goal
   * Functionalities that are required to satisfy an objective and dependencies between them
   * Replication constraints associated with different functionalities (mainly for redundancy)
   * Component types that provide functionalities (not explicit component instances)
   * Hardware categories and templates (not explicit hardware resources)
* At runtime, depending on the required functionalities and a set of component types, a set component instances and their inter-dependency is computed (this is the software graph)
* Different hardware resources (nodes that can be equipped with various devices) can ingress of egress a cluster dynamically at runtime; as such, at any given time there is a set of available harware resources with links between them (this is the hardware graph)
* The management problem being solved by CHARIOT is that of mapping the software graph onto the hardware graph while satisfying different system constraints

## Architectural Overview
CHARIOT consists of different entities that can be classified into three layers:

1. **Design layer**: This is the top-most layer and comprises a novel DSML (Domain Specific Modeling Language). This DSML is called CHARIOT-ML and it is built using the [Xtext framework](http://www.eclipse.org/Xtext/). CHARIOT-ML consists of (1) language grammars that are metamodels, and (2) interpreters that traverses user models to retrieve design-time system description.

2. **Data layer**: This is the middle layer. It comprises a well-defined data model that codifies the format in which system information (design-time system descriptions and runtime system representation) must be stored. CHARIOT currently uses [MongoDB](https://www.mongodb.com/) to store system information. This layer helps decouple the design layer (top) from the management layer (bottom).

  <img src="https://github.com/visor-vu/chariot/blob/master/LayeredOverview.png" width="45%" height="45%"/>

3. **Management layer (runtime)**: This is the bottom-most layer and is responsible for management of the runtime system. This layer comprises entities that facilitate autonomous resilience via a self-reconfiguration mechanism based on a closed *sense-plan-act* loop capable of (1) failure avoidance/masking using traditional redundancy mechanisms, (2) failure management to recover from failures, and (3) operations management to handle planned system updates. Entities in this layer can be differentiated into three categories. 
  * First category is the Monitoring Infrastructure, which comprises entities that help "sense" changes by detecting node ingress and egress. Current implementation of CHARIOT uses [ZooKeeper](https://zookeeper.apache.org/) to implement a dynamic monitoring infrastructure. 
  * Second category is the Management Engine, which "plans" for new solution when the system needs to reconfigure itself. CHARIOT uses [Z3 SMT Solver](https://github.com/Z3Prover/z3/) to implement the management engine. 
  * Third and final category is the Deployment Infrastructure, which comprises of distributed Deployment Managers (one per each node) that are responsible for "acting" on commands computed by the management engine. Each deployment manager is capable of managing local (node-specific) applications. Current implementation of CHARIOT using [ZeroMQ](http://zeromq.org/) as the middleware for communication between the management engine and deployment managers.

For interested readers, [this](http://www.dre.vanderbilt.edu/~schmidt/PDF/Pradhan_IoT.pdf) draft paper describes CHARIOT in much more detail.
