[![Build Status](https://travis-ci.org/visor-vu/chariot.svg?branch=master)](https://travis-ci.org/visor-vu/chariot)

# CHARIOT

CHARIOT is a holistic solution that facilitates design, development, and management of [extensible Cyber-Physical Systems (CPS)](http://etd.library.vbe.proxy.library.vanderbilt.edu/available/etd-11172016-154749/unrestricted/Pradhan.pdf). CHARIOT consists of different entities that can be classified into three layers:

1. **Design layer**: This is the top-most layer and comprises a novel DSML (Domain Specific Modeling Language) for extensible CPS.This DSML is called CHARIOT-ML and it is built using the [Xtext framework](http://www.eclipse.org/Xtext/). CHARIOT-ML consists of (1) language grammars that are metamodels using which users can design/model CPS, and (2) interpreters that traverses user models to retrieve design-time system description. Applications are modeled as software components that provide functionalities. Systems are modeled as composition of one or more functionalities.

<img src="https://github.com/visor-vu/chariot/blob/master/LayeredOverview.png" width="45%" height="45%"/>

2. **Data layer**: This is the middle layer. It comprises a well-defined data model that codifies the format in which system information (design-time system descriptions and runtime system representation) must be stored. CHARIOT currently uses [MongoDB](https://www.mongodb.com/) to store system information. This layer helps decouple the design layer (top) from the management layer (bottom) -- a design layer can comprise any modeling tool that generates system description that conforms to the data model; a management layer can be implemented in various ways and using varying technologies as long as its entities consume and produce data that conforms to the data model.

3. **Management layer (runtime)**: This is the bottom-most layer and comprises entities that facilitate autonomous resilience. In order to achieve autonomous resilience, CHARIOT implements a self-reconfiguration mechanism based on a closed *sense-plan-act* loop capable of (1) failure avoidance/masking using traditional redundancy mechanisms, (2) failure management to recover from failures, and (3) operations management to handle planned system updates. Entities in this layer can be differentiated into three categories. First category is the Monitoring Infrastructure, which comprises entities that help "sense" changes by detecting node ingress and egress. Current implementation of CHARIOT uses [ZooKeeper](https://zookeeper.apache.org/) to implement a dynamic monitoring infrastructure. Second category is the Management Engine, which "plans" for new solution when the system needs to reconfigure itself. CHARIOT uses [Z3 SMT Solver](https://github.com/Z3Prover/z3/) to implement the management engine. Third and final category is the Deployment Infrastructure, which comprises of distributed Deployment Managers (one per each node) that are responsible for "acting" on commands computed by the management engine. Each deployment manager is capable of managing local (node-specific) applications. Current implementation of CHARIOT using [ZeroMQ](http://zeromq.org/) as the middleware for communication between the management engine and deployment managers.

# Installation Guide
### MongoDB
1. Install MongoDB (tested with MongoDB version 3.2.11).
2. Install a MongoDB GUI (not required but makes it easier to check database contents). We use [Robomongo] (https://robomongo.org/download).

### CHARIOT-ML
1. Install Eclipse (tested with Eclipse [Mars 2](http://www.eclipse.org/downloads/packages/release/Mars/2)).
2. Install CHARIOT-DSML as an Eclipse plugin using the following update site:   
   http://scope.isis.vanderbilt.edu/chariot/eclipse/repository
   
   To install a new plugin in Eclipse you should go to [Help -> Install New Software...] and use above update site. Once this installation is complete you will be asked to restart Eclipse.
3. To check if the installation was successful, please perform the following tasks:
  * Run a local MongoDB server instance.
  * Clone the [CHARIOT examples](https://github.com/visor-vu/chariot-examples) repository.
  * Import any one of the available examples as existing project in your restarted Eclipse instance. When you browse the source folder you will see that CHARIOT-DSML icons are used for files and keywords are highlighted.
  * Run the CHARIOT-DSML interpreters by cleaning the project [Project -> Clean...].
  * Check MongoDB server for a database named *ConfigSpace* which should contain all system description information required by CHARIOT runtime.

### CHARIOT Runtime
1. Install [ZooKeeper](https://zookeeper.apache.org/releases.html). 

   *NOTE: This step is not required when running CHARIOT Runtime on simulation mode (Deployment managers receive actions from the management engine but do not start or stop application processes. Only runtime system representation is updated in the database).*
2. Install CHARIOTRuntime package using pip (Current implementation of CHARIOTRuntime uses Python 2.7.6).
```bash
sudo apt-get install python-pip
pip install CHARIOTRuntime
```

# Examples

Examples are available at https://github.com/visor-vu/chariot-examples
