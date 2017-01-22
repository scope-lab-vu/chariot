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

## Installation Guide
### MongoDB
1. Install MongoDB (tested with MongoDB version 3.2.11).

2. Install a MongoDB GUI (not required but makes it easier to check database contents). We use [Robomongo] (https://robomongo.org/download).

### CHARIOT-ML
1. Install Eclipse (tested with Eclipse [Mars 2](http://www.eclipse.org/downloads/packages/release/Mars/2)).

2. Install CHARIOT-ML as an Eclipse plugin using the following update site:   
   http://scope.isis.vanderbilt.edu/chariot/eclipse/repository
   
   To install a new plugin in Eclipse you should go to [Help -> Install New Software...] and use above update site. Once this installation is complete you will be asked to restart Eclipse.
   
4. To check if the installation was successful, please perform the following tasks:
  * Ensure that you have a running MongoDB server instance. This server can be local or remote. If remote, set *MONGO_ADDRESS* and *MONGO_PORT* environment variables accordingly. You might also have to restart your eclipse instance once these environment variables are set. 
  * Clone the [CHARIOT examples](https://github.com/visor-vu/chariot-examples) repository.
  * Import any one of the available examples as existing project in your restarted Eclipse instance [File->Import...->General->Existing Projects into Workspace]. When browsing the source folder you will see that CHARIOT-ML icons are used for files and keywords are highlighted.
  * Run the CHARIOT-ML interpreters by cleaning the project [Project -> Clean...].
  * Check MongoDB server for a database named *ConfigSpace* which should contain all system description information required by CHARIOT runtime.

### CHARIOT Runtime
Install chariot-runtime package using pip (Current implementation of chariot-runtime uses Python 2.7.6).
   ```bash
   sudo apt-get install python-dev
   sudo apt-get install python-pip
   sudo pip install chariot-runtime
   ```
Following are the commands installed as part of chariot-runtime:
* **chariot-dm**: This command starts the CHARIOT Deployment Manager
* **chariot-me**: This command starts the CHARIOT Management Engine
* **chariot-nm**: This command starts the CHARIOT Node Membership (this is a ZooKeeper client)
* **chariot-nmw**: This command starts the CHARIOT Node Membership Watcher (this is also a ZooKeeper client but it uses the watcher recipe)
* **chariot-rm**: This command starts the CHARIOT Resource Monitor to monitor resources (CPU, memory, network bandwidth) consumed by a CHARIOT Deployment Manager and CHARIOT Node Membership (current implementation requires PIDs of NM and DM to be passed via command line arguments)
* **chariot-sna**: This command should be used when running examples in simulation to simulate node activities (start and stop)

## Running the SmartPowerGrid example in Simulation Mode
Examples are available at https://github.com/visor-vu/chariot-examples. Follow the steps listed below to run the [SmartPowerGrid](https://github.com/visor-vu/chariot-examples/tree/master/SmartPowerGrid) example in simulation mode.

1. Clone the [CHARIOT examples](https://github.com/visor-vu/chariot-examples) repository.

2. Run a MongoDB server instance.

3. From inside SmartPowerGrid/scripts folder run the *SimulateNodeStartup* script. This will result in simulation of nine different nodes being started. 
   
   *NOTE: A closer inspection will show you that this script relies on the chariot-sna command installed as part of the chariot-runtime package. Please take a look at the names being assigned to each node.*
   
4. At this point you are advised to check your MongoDB server for the presence of *ConfigSpace* database, *Nodes* collection, and nine node-specific documents inside the *Nodes* collection.

5. Open Eclipse and import the SmartPowerGrid example as existing project 
   [File->Import...->General->Existing Projects into Workspace].
   
6. Run the CHARIOT-ML interpreters by cleaning the project [Project -> Clean...].

7. At this point you are advised to again check your MongoDB server for the presence of *ComponentTypes*, *GoalDescriptions*, and *NodeCategories* collections with documents representing the system description of the SmartParkingGrid example.

8. Open nine different terminals to simulate the nine different nodes started in *step 3*.

9. Start individual deployment managers on each terminal using the *chariot-dm* command installed as part of the chariot-runtime package. 

   The command shown below will start a deployment manager specific to node with name *pmu_z1_1*.
   ```bash
   chariot-dm -s pmu_z1_1
   ```

10. Open a new terminal and run the management engine for initial deployment.
   ```bash
   chariot-me -i
   ```
   This will result in computation of new deployment/configuration commands which will then be sent to corresponding deployment managers.
   
11. Check deployment manager terminals to verify that simulated actions were invoked.

12. At this point initial deployment is complete and now we can test autonomous resilience by injecting a node egress (failure). To do this, first start the management engine without initial deployment flag.
   ```bash
   chariot-me
   ```
   Now inject node failure use the *chariot-sna* command as shown below (for *node ied_z1_1*).
   ```bash
   chariot-sna -n ied_z1_1 -a stop
   ```
   This will trigger the chariot-runtime's self-reconfiguration mechanism. You can verify this by checking the ManagementEngine's output.
   
13. Above step tested CHARIOT's failure management capability. CHARIOT is also capable of operations management (i.e., managing planned system updates); in order to test this we can simulate a hardware update scenario by performing node ingress (adding a node). In this example if we add a PMU node to any of the three protection zones using their default templates, a corresponding PMU component instance will be added due to per-node replication (see [here]() for detail about this replication constraint).
  ```bash
  chariot-sna -n pmu_z1_2 -t default_pmu_z1 -p 7010 -a start
  ```
  Above command will trigger the chariot-runtime's self-reconfiguration mechanism. You can verify this by checking the ManagementEngine's output.
   
## Running the SmartParkingBasic example in Non-simulation Mode
Follow the steps listed below to run the [SmartParkingBasic](https://github.com/visor-vu/chariot-examples/tree/master/SmartParkingBasic) example in non-simulation (i.e., distribtued) mode.

### Starting the Server Nodes
Server nodes (i.e., nodes that host MongoDB server, ZooKeeper server, CHARIOT Node Membership Watcher, and CHARIOT Management Engine) should be separate from the compute nodes (i.e, nodes that hosts different applications).

1. Start a node to host a MongoDB server
  * [optional] Update hostname (/etc/hostname) to something meaningful (e.g. mongo-server)
  * Install MongoDB (see [this](#mongodb))
  * Run an instance of the MongoDB server
  
2. Start a node to host a CHARIOT Management Engine
  * [optional] Update hostname (/etc/hostname) to something meaningful (e.g. management-engine)
  * Update hosts file (/etc/hosts) to add information about mongo-server node
  * Install CHARIOT runtime (see [this](#chariot-runtime))

3. Start a node to host a ZooKeeper server and a CHARIOT Node Membership Watcher
  * [optional] Update hostname (/etc/hostname) to something meaningful (e.g. monitoring-server)
  * Update hosts file (/etc/hosts) to add information about mongo-server and management-engine nodes
  * Install [ZooKeeper](https://zookeeper.apache.org/releases.html)
  
    ```bash
    sudo apt-get install zookeeper
    sudo apt-get install zookeeperd
    ```
  * Install CHARIOT runtime (see [this](#chariot-runtime)) and update configuration file located in /etc/chariot/chariot.conf
  * Use update-rc.d to ensure an instance of CHARIOT Node Membership Watcher is launched at boot
  
    ```bash
    cd /etc/init.d
    sudo update-rc.d chariot-nmw defaults 99
    ```
  * Restart the node, which will result in execution of an instance each of ZooKeeper server and CHARIOT Node Membership Watcher
  
  *NOTE: A CHARIOT Node Membership Watcher does not need to run on the same node as a ZooKeeper server. We do so for simplicity.*

### Starting the Compute Nodes
Compute nodes are nodes that hosts different applications. Since CHARIOT runtime uses its deployment infrastructure to perform application management, each compute node hosts an instance of the CHARIOT Deployment Manager. Futhermore, each compute node also hosts an instance of the CHARIOT Node Membership, which in essence is a ZooKeeper client and is part of the CHARIOT monitoring infrastructure. Follow the steps listed below for each compute node:

1. [optional] Start the node and update hostname (/etc/hostname) to something meaningful (e.g. node-1 .. node-5)

2. Update hosts file (/etc/hosts) to add information about mongo-server and monitoring-server

3. Install CHARIOT runtime (see [this](#chariot-runtime)) and update configuration file located in /etc/chariot/chariot.conf

4. Use update-rc.d to ensure an instance of CHARIOT Deployment Manager and CHARIOT Node Membership is launched at boot
  ```bash
  cd /etc/init.d
  sudo update-rc.d chariot-nm defaults 99
  sudo update-rc.d chariot-dm defaults 99
  ```

5. Restart the node, which will result in execution of an instance of CHARIOT Deployment Manager and CHARIOT Node Membership

Once above set of steps are completed for every compute node, check the MongoDB server for the presence of *ConfigSpace* database and *Nodes* collection. This collection should have a document each for every compute node.

### Generating the System Description and Performing Initial Deployment
Now that server nodes and compute nodes have been setup successfully, we must generate the required system description of the SmartParkingBasic example using CHARIOT-ML and then perform the initial deployment of the SmartParkingBasic system.

1. In any of the existing server nodes or a completely new node, install CHARIOT-ML (see [here](#chariot-ml)).

2. Open Eclipse and import the SmartParkingBasic example as existing project 
   [File->Import...->General->Existing Projects into Workspace].
   
3. Run the CHARIOT-ML interpreters by cleaning the project [Project -> Clean...].

4. At this point you are advised to again check your MongoDB server for the presence of *ComponentTypes*, *GoalDescriptions*, and *NodeCategories* collections with documents representing the system description of the SmartParkingGrid example.

5. Switch to the *management-engine* node (start in step 2 of [this](#starting-the-server-nodes) section) and run the management engine for initial deployment.
   ```bash
   chariot-me -i
   ```
   This will result in computation of new deployment/configuration commands which will then be sent to corresponding deployment managers.
   
6. Check deployment manager logs (located at /etc/chariot/logs of remote compute nodes) to verify that deployement actions were taken. At this point initial deployment of the SmartParkingBasic system is complete.

### Testing Node Failure (egress)
Now that the initial deployment is successfully performed, we can test node egress (node failure) by stopping one of the five compute nodes.

1. Start the management-engine without initial deployment flag.
   ```bash
   chariot-me
   ```
2. Stop one of the five compute nodes. This should result in following sequence of actions:
  * The CHARIOT Node Membership Watcher running on the *monitoring-server* node will detect the node failure, update the database, and invoke the CHARIOT Management Engine.
  * The CHARIOT Management Engine will compute a new solution, if required (keep adding failures to ensure reconfiguration event). Based on the new solution, deployment actions are sent to respective CHARIOT Deployment Managers.
  * The CHARIOT Deployment Managers will perform received deployment actions.
  
### Testing Node Addition (ingress)
To test node ingress (addition of a node), just follow steps listed [here](#starting-the-compute-nodes) for the new node. This should result in following sequence of actions:
* The CHARIOT Node Membership Watcher running on the *monitoring-server* node will detect the node addition, update the database, and invoke the CHARIOT Management Engine.
* The CHARIOT Management Engine will compute a new solution, if required. Based on the new solution, deployment actions are sent to respective CHARIOT Deployment Managers.
* The CHARIOT Deployment Managers will perform received deployment actions.
