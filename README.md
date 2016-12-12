[![Build Status](https://travis-ci.org/visor-vu/chariot.svg?branch=master)](https://travis-ci.org/visor-vu/chariot)

# CHARIOT

CHARIOT is a holistic solution that facilitates design, development, and management of [extensible Cyber-Physical Systems (CPS)](http://etd.library.vbe.proxy.library.vanderbilt.edu/available/etd-11172016-154749/unrestricted/Pradhan.pdf). CHARIOT consists of different entities that can be classified into three layers:

<img src="https://github.com/visor-vu/chariot/blob/master/LayeredOverview.png" width="45%" height="45%"/>

- Design layer: This is the top-most layer and comprises a novel DSML (Domain Specific Modeling Language) for extensible CPS.This DSML is called CHARIOT-ML and it is built using the [Xtext framework](http://www.eclipse.org/Xtext/). CHARIOT-ML consists of (1) language grammars that are metamodels using which users can design/model CPS, and (2) interpreters that traverses user models to retrieve design-time system description. Applications are modeled as software components that provide functionalities. Systems are modeled as composition of one or more functionalities.

- Data layer: This is the middle layer. It comprises a well-defined data model that codifies the format in which system information (design-time system descriptions and runtime system representation) must be stored. CHARIOT currently uses [MongoDB](https://www.mongodb.com/) to store system information. This layer helps decouple the design layer (top) from the management layer (bottom) -- a design layer can comprise any modeling tool that generates system description that conforms to the data model; a management layer can be implemented in various ways and using varying technologies as long as its entities consume and produce data that conforms to the data model.

- Management layer (runtime): This is the bottom-most layer and comprises entities that facilitate autonomous resilience. In order to achieve autonomous resilience, CHARIOT implements a self-reconfiguration mechanism based on a closed sense-plan-act loop capable of (1) failure avoidance/masking using traditional redundancy mechanisms, (2) failure management to recover from failures, and (3) operations management to handle planned system updates. Entities in this layer can be differentiated into three categories. First category is the Monitoring Infrastructure, which comprises entities that help "sense" changes by detecting node ingress and egress. Current implementation of CHARIOT uses [ZooKeeper](https://zookeeper.apache.org/) to implement a dynamic monitoring infrastructure. Second category is the Management Engine, which "plans" for new solution when the system needs to reconfigure itself. CHARIOT uses [Z3 SMT Solver](https://github.com/Z3Prover/z3/) to implement the management engine. Third and final category is the Deployment Infrastructure, which comprises of distributed Deployment Managers (one per each node) that are responsible for "acting" on commands computed by the management engine. Each deployment manager is capable of managing local (node-specific) applications. Current implementation of CHARIOT using [ZeroMQ](http://zeromq.org/) as the middleware for communication between the management engine and deployment managers.

# Summary of dependencies

Chariot uses the following other open source projects

- Xtext
- Z3

For further information please see http://chariot.isis.vanderbilt.edu/

# Examples

Examples are available at https://github.com/visor-vu/chariot-examples
