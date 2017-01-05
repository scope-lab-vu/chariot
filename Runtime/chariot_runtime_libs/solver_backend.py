__author__ = "Subhav Pradhan"

import operator
import datetime
import copy
from operator import attrgetter
from chariot_helpers import Serialize
from logger import get_logger

logger = get_logger("solver_backend")

class GoalDescription:
    name = None
    replicationConstraints = None           # List of constraints read from the database.
    objectives = None
    functionalityInstances = None           # List of functionality instances.
    computedFunctionalities = None          # List of functionalities for which instances have been computed.
    compTypesToFuncInstances = None         # List of tuple <list of component type name,
                                            #                list of functionality instance names>.
    componentInstances = None               # List of component instances.
    componentInstanceDependencies = None
    functionalityConstraints = None         # List of constraints in terms of functionality instances. This list
                                            # will be used to generate solver constraints, which should be in terms
                                            # of component instances
    funcInstancesToCompInstances = None     # Dictionary with key = functionality instance name, and value = component
                                            # instance name.

    # TODO: Some notion of componentConstraints will also be required to store constraints related to multiple
    # TODO: components providing same functionality.

    def __init__(self):
        self.name = ""
        self.replicationConstraints = list()
        self.objectives = list()
        self.functionalityInstances = list()
        self.computedFunctionalities = list()
        self.compTypesToFuncInstances = list()
        self.componentInstances = list()
        self.componentInstanceDependencies = dict()
        self.functionalityConstraints = list()
        self.funcInstancesToCompInstances = dict()

    def get_objectives(self):
        return self.objectives

    def get_functionality_instances(self):
        return self.functionalityInstances

    def get_functionality_constraints(self):
        return self.functionalityConstraints

    def get_component_instances(self):
        return self.componentInstances

    def get_replication_constraints(self):
        return self.replicationConstraints

    def get_component_instance_dependencies(self):
        return self.componentInstanceDependencies

    # This function computes dependencies for each component instance and returns a dictionary in which each
    # entry is a tuple <component instance name, list of names of component instances it depends on>.
    def compute_component_instance_dependencies(self):
        if len(self.componentInstanceDependencies) > 0:
            logger.info ("Recomputing component instance dependencies")
            self.componentInstanceDependencies.clear()  # Emptying component instances list.

        for compInst in self.componentInstances:
            compInstDependencies = list()
            # Get functionality instance object corresponding to componentInstance.
            functionalityInstance = None
            for funcInst in self.functionalityInstances:
                if funcInst.name == compInst.functionalityInstanceName:
                    functionalityInstance = funcInst
                    break

            # Collect functionality dependencies if above functionalityInstance is NOT a voter.
            # Check validity of above functionalityInstance.
            if functionalityInstance is not None and not functionalityInstance.isVoter:
                functionalityDependencies = list()
                for obj in self.objectives:
                    for func in obj.functionalities:
                        if func.name == functionalityInstance.functionalityName:
                            for dependency in func.dependsOn:
                                functionalityDependencies.append(dependency)    # Append because a functionality might
                                                                                # be present in multiple objectives.

                # For each functionality in above collected functionality dependencies, find and store corresponding
                # functionality instances in retVal.
                for funcDependency in functionalityDependencies:
                    voterDependencyHandled = False
                    for funcInst in self.functionalityInstances:
                        if funcInst.functionalityName == funcDependency:
                            # Handle scenario where the functionality dependency is a voter. In this case the
                            # functionality instance should have dependency related to the voter and not funcInst.
                            if "VOTER_REPLICATION" in self.check_replication_constraint(funcInst.functionalityName):
                                if not voterDependencyHandled:
                                    voterFuncInstName = self.find_voter_functionality_instance_name(funcInst.functionalityName)
                                    if voterFuncInstName is not None and \
                                                    voterFuncInstName in self.funcInstancesToCompInstances:
                                        compInstDependencies.append(self.funcInstancesToCompInstances[voterFuncInstName])
                                    voterDependencyHandled = True
                            else:
                                if funcInst.name in self.funcInstancesToCompInstances:
                                    compInstDependencies.append(self.funcInstancesToCompInstances[funcInst.name])
            elif functionalityInstance.isVoter:
                # If functionality instance is a voter, establish dependency between functionality instances that
                # use the voter and the voter itself. Relying on consistent naming convention.
                for funcInst in self.functionalityInstances:
                    if functionalityInstance.name != funcInst.name and functionalityInstance.name[:-8] in funcInst.name:
                        compInstDependencies.append(self.funcInstancesToCompInstances[funcInst.name])

            self.componentInstanceDependencies[compInst.name] = compInstDependencies

    # This function returns name of the voter functionality instance corresponding to the given functionality.
    def find_voter_functionality_instance_name(self, functionality):
        retVal = None

        for funcInst in self.functionalityInstances:
            if functionality in funcInst.name and "_voter_service" in funcInst.name:
                retVal = funcInst.name
                break

        return retVal

    # This function finds and returns name of all ACTIVE nodes of category nodeCategory.
    @staticmethod
    def get_node_names(nodeCategory, nodes, nodeTemplates):
        retval = list()

        for node in nodes:
            if node.status == "ACTIVE":
                categoryFound = None

                for nodeTemplate in nodeTemplates:
                    if node.nodeTemplate == nodeTemplate.name:
                        categoryFound = nodeTemplate.nodeCategory

                if categoryFound == nodeCategory:
                    retval.append(node)

        return retval

    # This function computes functionality instances and stores them in functionalityInstances list.
    def compute_functionality_instances(self, nodes, nodeTemplates):
        if len(self.functionalityInstances) > 0:
            logger.info ("Recomputing functionality instances")
            del self.functionalityInstances[:]  # Emptying functionality instances list.

        for objective in self.objectives:
            # Handle replication of functionalities.
            self.handle_functionality_instances_replication (objective, nodes, nodeTemplates)

            # Handle collocation constraints.
            # NOTE: We currently do not use collocation constraint. We only use replication constraints.
            self.handle_functionality_instances_collocation (objective)

    # This function computes component instances and stores in componentInstances list.
    def compute_component_instances(self, componentTypes):
        if len(self.componentInstances) > 0:
            logger.info ("Recomputing component instances")
            del self.componentInstances[:]  # Emptying component instances list.

        for functionalityInstance in self.functionalityInstances:
            # List of component types that provides the functionality associated with the functionalityInstance.
            providingComponentTypes = list()

            # Store component types for voter and consensus service providers.
            if functionalityInstance.isVoter or functionalityInstance.isConsensusProvider:
                componentInstanceToAdd = ComponentInstance()
                componentInstanceToAdd.name = functionalityInstance.componentType + "_" + \
                                              functionalityInstance.name.replace("func", "comp")
                componentInstanceToAdd.type = functionalityInstance.componentType
                componentInstanceToAdd.status = "TO_BE_DEPLOYED"
                componentInstanceToAdd.functionalityInstanceName = functionalityInstance.name
                self.componentInstances.append(componentInstanceToAdd)
                self.funcInstancesToCompInstances[functionalityInstance.name] = componentInstanceToAdd.name
            else:
                # If not voter or consensus service provider, then find component types that provide
                # functionality associated with functionalityInstance.
                for componentType in componentTypes:
                    if componentType.providedFunctionality == functionalityInstance.functionalityName:
                        providingComponentTypes.append(componentType)

            for componentType in providingComponentTypes:
                componentName = componentType.name + "_" + functionalityInstance.name.replace("func", "comp")
                componentInstanceToAdd = ComponentInstance()
                componentInstanceToAdd.name = componentName
                componentInstanceToAdd.type = componentType.name
                componentInstanceToAdd.status = "TO_BE_DEPLOYED"
                componentInstanceToAdd.alwaysDeployOnNode = functionalityInstance.alwaysDeployOnNode
                componentInstanceToAdd.functionalityInstanceName = functionalityInstance.name
                componentInstanceToAdd.mustDeploy = functionalityInstance.mustDeploy
                self.componentInstances.append(componentInstanceToAdd)
                self.funcInstancesToCompInstances[functionalityInstance.name] = componentInstanceToAdd.name

            # TODO: If number of component instances generated by above loop is greater than 1, add
            # TODO: EXACTLY 1 out of N constraint for the component instances.

    # This function handles creation of functionality instances associated with replication constraints,
    # including singleton functionality instances.
    def handle_functionality_instances_replication(self, objective, nodes, nodeTemplates):
        for functionality in objective.functionalities:
            if functionality.name not in self.computedFunctionalities:
                # Check if functionality has any associated replication constraint. If it does then
                # instantiate required number of instances. If not then instantiate single instance.
                replicationConstraints = self.check_replication_constraint(functionality.name)
                if len(replicationConstraints) > 0:
                    # If there are replications constraint(s) then apply each one of the constraint.
                    for constraint in replicationConstraints:
                        if constraint.kind == "PER_NODE_REPLICATION":
                            # If perNode replication constraint, then use node categories to get all nodes of interest.
                            for nodeCategory in constraint.nodeCategories:
                                for node in self.get_node_names(nodeCategory, nodes, nodeTemplates):
                                    # Only create functionality instance and associated constraint if node is ACTIVE.
                                    if node.status == "ACTIVE":
                                        functionalityInstanceToAdd = FunctionalityInstance()
                                        functionalityInstanceToAdd.name = functionality.name + "_func_instance_" + node.name
                                        functionalityInstanceToAdd.functionalityName = functionality.name
                                        functionalityInstanceToAdd.objectiveName = objective.name
                                        functionalityInstanceToAdd.alwaysDeployOnNode = node.name
                                        functionalityInstanceToAdd.mustDeploy = True
                                        self.functionalityInstances.append(functionalityInstanceToAdd)
                                        self.computedFunctionalities.append(functionalityInstanceToAdd.functionalityName)
                                        self.functionalityConstraints.append(("assign",
                                                                              functionalityInstanceToAdd.name,
                                                                              node.name))
                        else:
                            initialNumInstances = 0
                            rangeBased = False

                            # Set initial number of functionality instances that needs to be generated.
                            # If exact number given then we use that, otherwise if a range is given then
                            # we use the maximum of the range as our initial number.
                            if (constraint.numInstances != 0):
                                initialNumInstances = constraint.numInstances
                            else:
                                rangeBased = True
                                initialNumInstances = constraint.maxInstances

                            if initialNumInstances != 0:
                                constraintKind = None

                                # Handle VOTER replication scenario by generating a corresponding functionality
                                # instance. This is done outside the loop as we want one voter. However, for
                                # CONSENSUS replication, we generate one consensus provider per functionality
                                # instance. Therefore, this scenario is handled inside the loop. For both, voter
                                # and consensus provider functionality instances, functionality will be empty as
                                # we do not want the solver to use functionality in order to determine correct
                                # component type to instantiate. For these functionality instances we know exactly
                                # which component type to instantiate (componentType). CLUSTER replication does not
                                # require any special care.
                                if constraint.kind == "VOTER_REPLICATION":
                                    constraintKind = "voter"
                                    voterInstanceToAdd = FunctionalityInstance()
                                    voterInstanceToAdd.name = functionality.name + "_func_instance_voter_service"
                                    voterInstanceToAdd.objectiveName = objective.name
                                    voterInstanceToAdd.isVoter = True
                                    voterInstanceToAdd.componentType = constraint.serviceComponentType
                                    self.functionalityInstances.append(voterInstanceToAdd)
                                    #self.computedFunctionalities.append()  # No functionality to add.
                                if constraint.kind == "CLUSTER_REPLICATION": constraintKind = "cluster"

                                tmpFunctionalityInstancesList = list()
                                tmpConsensusServiceInstancesList = list()
                                for i in range(0, initialNumInstances):
                                    # If consensus cluster then generate consensus provider functionality instance.
                                    consensusInstanceToAdd = None
                                    if constraint.kind == "CONSENSUS_REPLICATION":
                                        constraintKind = "consensus"
                                        consensusInstanceToAdd = FunctionalityInstance()
                                        consensusInstanceToAdd.name = \
                                            functionality.name + "_func_instance_consensus_service_" + str(i)
                                        consensusInstanceToAdd.objectiveName = objective.name
                                        consensusInstanceToAdd.isConsensusProvider = True
                                        consensusInstanceToAdd.componentType = constraint.serviceComponentType
                                        self.functionalityInstances.append(consensusInstanceToAdd)
                                        tmpConsensusServiceInstancesList.append(consensusInstanceToAdd.name)
                                        #self.computedFunctionalities.append()  # No functionality to add.

                                    functionalityInstanceToAdd = FunctionalityInstance()
                                    functionalityInstanceToAdd.name = \
                                        functionality.name + "_func_instance_" + constraintKind + "_" + str(i)
                                    functionalityInstanceToAdd.functionalityName = functionality.name
                                    functionalityInstanceToAdd.objectiveName = objective.name
                                    if not rangeBased:
                                        functionalityInstanceToAdd.mustDeploy = True
                                    self.functionalityInstances.append(functionalityInstanceToAdd)
                                    self.computedFunctionalities.append(functionalityInstanceToAdd.functionalityName)
                                    tmpFunctionalityInstancesList.append(functionalityInstanceToAdd.name)

                                    # If consensus cluster then add a constraint such that the consensus provider
                                    # functionality instance and associated replication functionality instance
                                    # created above are always collocated.
                                    if consensusInstanceToAdd is not None:
                                        self.functionalityConstraints.append(("collocate",
                                                                              functionalityInstanceToAdd.name,
                                                                              consensusInstanceToAdd.name))
                                        self.functionalityConstraints.append(("implies",
                                                                              functionalityInstanceToAdd.name,
                                                                              consensusInstanceToAdd.name))

                                if rangeBased:
                                    #if len(tmpConsensusServiceInstancesList) != 0:
                                    #    self.functionalityConstraints.append(("atleast",
                                    #                                          constraint.minInstances,
                                    #                                          tmpConsensusServiceInstancesList,
                                    #                                          objective.name))

                                    self.functionalityConstraints.append(("atleast",
                                                                          constraint.minInstances,
                                                                          constraint.maxInstances,
                                                                          tmpFunctionalityInstancesList,
                                                                          objective.name))

                                self.functionalityConstraints.append(("distribute", tmpFunctionalityInstancesList))
                else:
                    # Functionality doesn't have perNode constraint or replication constraint, so generate
                    # singleton functionality instance.
                    functionalityInstanceToAdd = FunctionalityInstance()
                    functionalityInstanceToAdd.name = functionality.name + "_func_instance"
                    functionalityInstanceToAdd.functionalityName = functionality.name
                    functionalityInstanceToAdd.objectiveName = objective.name
                    functionalityInstanceToAdd.mustDeploy = True
                    self.functionalityInstances.append(functionalityInstanceToAdd)
                    self.computedFunctionalities.append(functionalityInstanceToAdd.functionalityName)

    # This function handles collocation of functionality instances.
    def handle_functionality_instances_collocation(self, objective):
        for functionality in objective.functionalities:
            for collocationConstraint in self.check_collocation_constraint(functionality):
                functionalityRequiringCollocation = collocationConstraint.functionalities[0]
                functionalityToBeCollocated = collocationConstraint.functionalities[1]

                # Get all functionality instances for above two functionalities.
                functionalityInstancesRequiringCollocation = \
                    self.get_functionality_instances_name(functionalityRequiringCollocation)
                functionalityInstancesToBeCollocated = \
                    self.get_functionality_instances_name(functionalityToBeCollocated)

                for functionalityInstanceRequiringCollocation in functionalityInstancesRequiringCollocation:
                    constraintListToAdd = list()
                    for functionalityInstanceToBeCollocated in functionalityInstancesToBeCollocated:
                        constraintToAdd = \
                            (functionalityInstanceRequiringCollocation, functionalityInstanceToBeCollocated)
                        constraintListToAdd.append(constraintToAdd)
                    self.functionalityConstraints.append(("collocate", constraintListToAdd))

    # This function checks if the functionality with the given name has any replication constraint. Returns a list of
    # replication constraints.
    def check_replication_constraint(self, functionalityName):
        retval = list()

        for replConstraint in self.replicationConstraints:
            if functionalityName == replConstraint.functionality:
                if replConstraint.kind == "VOTER_REPLICATION" or \
                   replConstraint.kind == "CONSENSUS_REPLICATION" or \
                   replConstraint.kind == "CLUSTER_REPLICATION" or \
                   replConstraint.kind == "PER_NODE_REPLICATION":
                    retval.append(replConstraint)

        return retval

    # This function checks if the given functionality has any collocation constraint. Returns a list of
    # collocation constraint.
    def check_collocation_constraint(self, functionality):
        retval = list()

        for replConstraint in self.replicationConstraints:
            if functionality.name == replConstraint.functionality and replConstraint.kind == "NODE_COLLOCATION":
                retval.append(replConstraint)

        return retval

    # This function returns name of ALL functionality instances for given functionality.
    def get_functionality_instances_name(self, functionality):
        retval = list()

        for functionalityInstance in self.functionalityInstances:
            if functionalityInstance.functionalityName == functionality:
                retval.append(functionalityInstance.name)

        return retval

class ReplicationConstraint:
    kind = None
    functionality = None        # Functionality name
    minInstances = None
    maxInstances = None
    numInstances = None
    serviceComponentType = None
    nodeCategories = None       # List of node categories. This is only valid for per node constraints.


    def __init__(self):
        self.kind = ""
        self.functionality = ""
        self.minInstances = 0
        self.maxInstances = 0
        self.numInstances = 0
        self.serviceComponentType = ""
        self.nodeCategories = list()

class Objective:
    name = None
    functionalities = None  # List of functionality objects.

    def __init__(self):
        self.name = ""
        self.functionalities = list()

class Functionality:
    name = None
    dependsOn = None


    def __init__(self):
        self.name = ""
        self.dependsOn = list()

    # This function returns constraints associated with a functionality.
    def get_constraints(self, constraints):
        retval = list()
        for constraint in constraints:
            if self.name in constraint.functionalities:
                retval.append(constraint)
        return retval

# This class represents instances of functionalities. A functionality with replication constraint
# can have multiple functionality instances. Also, two objectives with same functionality will result
# in single functionality instance. A functionality instance can be defined as instantiation of a
# functionality in the run-time via appropriate component instance.
class FunctionalityInstance:
    name = None
    objectiveName = None
    functionalityName = None        # This attribute will be empty for voter and consensus provider
                                    # functionality instances.

    alwaysDeployOnNode = None       # This attribute is only valid if functionality instance is
                                    # tied to a node as part of per node replication pattern.

    isVoter = None                  # This flag determines if a functionality instance is related
                                    # to a voter.

    isConsensusProvider = None      # This flag determines if a functionality instance is related
                                    # to a consensus provider.

    componentType = None            # This attribute is only valid if isVoter or isConsensusProvider
                                    # is true. This allows us to directly associate a functionality
                                    # instance with the specific component type in order to generate
                                    # required component instance.

    mustDeploy = None               # This flag determines if a functionality instance should always be
                                    # available and therefore deployed. This will be false only for
                                    # functionality instances that are not part of atleast replication.

    def __init__(self):
        self.name = ""
        self.functionalityName = ""
        self.objectiveName = ""
        self.alwaysDeployOnNode = ""
        self.isVoter = False
        self.isConsensusProvider = False
        self.componentType = ""
        self.mustDeploy = False

class Process:
    name = None
    pid = None
    status = None
    componentInstances = None   # List of component instances.

    def __init__(self):
        self.name = ""
        self.pid = -1
        self.status = ""
        self.componentInstances = list()

class Node:
    name = None
    nodeTemplate = None
    status = None
    processes = None            # List of processes instances.

    def __init__(self):
        self.name = ""
        self.nodeTemplate = ""
        self.status = ""
        self.processes = list()

    # This function returns a list of tuple (cumulative resource type, value)
    # NOTE: Current implementation only considers one resource type -- Memory.
    def compute_cumulative_provisions(self, nodeTemplates):
        retval = list()

        for template in nodeTemplates:
            if template.name == self.nodeTemplate:
                if template.availableMemory[0] > 0:
                    retval.append(("memory", template.availableMemory[0]))
        return retval

    # This function returns a list of devices hosted by a node.
    def compute_device_provisions(self, nodeTemplates):
        retval = list()

        for template in nodeTemplates:
            if template.name == self.nodeTemplate:
                for device in template.devices:
                    # Only return devices that are active. (Skip for now)
                    #if device.status == "ACTIVE":
                    retval.append(device)

        return retval

class NodeTemplate:
    name = None
    nodeCategory = None
    availableMemory = None      # Tuple (amount, unit).
    availableStorage = None     # Tuple (amount, unit).
    os = None
    middleware = None
    artifacts = None            # List of tuple (name, location)
    devices = None              # List of devices.

    def __init__(self):
        self.name = ""
        self.nodeCategory = ""
        self.availableMemory = (0, "")
        self.availableStorage = (0, "")
        self.os = ""
        self.middleware = ""
        self.artifacts = list()
        self.devices = list()

class Device:
    name = None
    artifacts = None            # List of device related artifacts as tuple (name, location).
    status = None

    def __init__(self):
        self.name = ""
        self.artifacts = list()
        self.status = ""

class ComponentType:
    name = None
    providedFunctionality = None
    requiredMemory = None        # Tuple (amount, unit).
    requiredStorage = None       # Tuple (amount, unit).
    requiredOS = None
    requiredMiddleware = None
    requiredArtifacts = None     # List of strings.
    requiredDevices = None       # List of strings.
    startScript = None
    stopScript = None
    period = None                   # Tuple (amount, unit)
    deadline = None                 # Tuple (amount, unit)

    def __init__(self):
        self.name = ""
        self.providedFunctionality = ""
        self.requiredMemory = (0, "")
        self.requiredStorage = (0, "")
        self.requiredOS = ""
        self.requiredMiddleware = ""
        self.requiredArtifacts = list()
        self.requiredDevices = list()
        self.startScript = ""
        self.stopScript = ""
        self.period = (0.0, "")
        self.deadline = (0.0, "")

class ComponentInstance:
    name = None
    type = None
    status = None
    functionalityInstanceName = None    # Name of functionality instance (i.e. functionality) provided by a component
                                        # instance. We currently assume one functionality per component instance.

    alwaysDeployOnNode = None           # This attribute is only valid if functionality instance is
                                        # tied to a node as part of a per node replication pattern.

    mustDeploy = None                   # This flag determines if a component instance should always be
                                        # available and therefore deployed. This will be false only for
                                        # component instances that are not part of atleast replication.

    def __init__(self):
        self.name = ""
        self.type = ""
        self.status = ""
        self.functionalityInstanceName = ""
        self.alwaysDeployOnNode = ""
        self.mustDeploy = False

class SolverBackend:
    # List of entities constructed from information in the database.
    goalDescriptions = None
    nodes = None
    nodeTemplates = None
    objectives = None
    componentTypes = None

    # Generated lists. These lists store cross goal description instances.
    functionalityInstances = None
    functionalityConstraints = None
    componentInstances = None
    componentInstanceDependencies = None
    constraints = None

    # Deployment representation as an adjacency matrix (NUM_OF_COMPONENTS X NUM_OF_NODES).
    c2n = None

    # List of indexes of component instances that must always be deployed.
    mustDeployComponentInstancesIndex = None

    # Caching names <-> indices.
    objectiveName2Index = None
    componentInstName2Index = None
    nodeName2Index = None
    processName2Index = None

    # Other mappings for easy access to info component instance -> process -> node.
    # Depends on the fact that process names are unique.
    componentInstIndex2ProcessIndex = None
    processIndex2NodeIndex = None

    # R x N matrices of cumulative and comparative (device) resources provided by nodes.
    nodeCumProvidedResources = None
    nodeCompProvidedResources = None

    # R x C matrices of cumulative and comparative resoruces required by component instances.
    componentInstCumRequiredResources = None
    componentInstCompRequiredResources = None

    # List of estimated utilization of component instances.
    componentInstUtilization = None

    # List of reliability computed for nodes.
    nodeReliability = None

    # List of reliability computed for devices. Devices are comparative resources.
    # Not all comparative resources are devices. As such, reliability for other comparative
    # resources will always be 0.
    compResourceReliability = None

    # Mapping (using dictionary) between resources and nodes, and resources and components.
    cumResource2nodeIndex = None
    compResource2nodeIndex = None
    cumResource2componentInstIndex = None
    compResource2componentInstIndex = None

    def __init__(self):
        self.goalDescriptions = list()
        self.nodes = list()
        self.nodeTemplates = list()
        self.objectives = list()
        self.componentTypes = list()

        self.functionalityInstances = list()
        self.functionalityConstraints = list()
        self.componentInstances = list()
        self.componentInstanceDependencies = dict()

        self.c2n = list(list())

        self.mustDeployComponentInstancesIndex = list()

        self.objectiveName2Index = dict()
        self.componentInstName2Index = dict()
        self.nodeName2Index = dict()
        self.processName2Index = dict()

        self.componentInstIndex2ProcessIndex = dict()
        self.processIndex2NodeIndex = dict()

        self.nodeCumProvidedResources = list(list())
        self.nodeCompProvidedResources = list(list())           # This matrix is only for devices.

        self.componentInstCumRequiredResources = list(list())
        self.componentInstCompRequiredResources = list(list())

        self.componentInstUtilization = list()

        self.nodeReliability = list()
        self.compResourceReliability = list(list())             # This matrix is only for devices.

        # Dict with cumulative resource name as key and value is a list of tuple
        # (node index, provided resource value).
        self.cumResource2nodeIndex = dict()

        # Dict with comparative resource name as key and value is a list of node index.
        self.compResource2nodeIndex = dict()

        # Dict with cumulative resource name as key and value is a list of tuple
        # (component instance index, provided resource value).
        self.cumResource2componentInstIndex = dict()

        # Dict with comparative resource name as key and value is a list of component instance index.
        self.compResource2componentInstIndex = dict()

    # Helper to return nodes that are alive.
    def get_alive_nodes(self):
        aliveNodes = list()
        for node in self.nodes:
            if node.status == "ACTIVE":
                aliveNodes.append(node)

        return aliveNodes

    # Helper to add component instance to componentInstances list. This function also updates status when required.
    def add_component_instance(self, componentInstanceToAdd, updateStatus):
        existingCompInstances = list()
        for compInst in self.componentInstances:
            existingCompInstances.append(compInst.name)

        if componentInstanceToAdd.name not in existingCompInstances:
            self.componentInstances.append(componentInstanceToAdd)
        else:
            if updateStatus:
                for compInst in self.componentInstances:
                    if compInst.name == componentInstanceToAdd.name and \
                                    compInst.status != componentInstanceToAdd.status:
                        compInst.status = componentInstanceToAdd.status

    # Given a name, return matching component instance.
    def get_component_instance(self, name):
        for componentInstance in self.componentInstances:
            if name == componentInstance.name:
                return componentInstance

        return None

    # This function returns start and stop script of a component.
    def get_component_scripts(self, type):
        for componentType in self.componentTypes:
            if type == componentType.name:
                return [componentType.startScript, componentType.stopScript]

    # This function loads different state related information.
    def load_state(self, db):
        self.load_node_templates(db)
        self.load_nodes_info(db)                        # IMPORTANT: This ordering between template and nodes matter.
        self.load_component_instances(db)               # Load any existing component instances
        self.load_component_types(db)
        self.load_goal_descriptions(db)                 # Any required component instances that are were not present
                                                        # in existing state (loaded as part of load_component_instances)
                                                        # will be generated here.
        self.load_component_to_node_assignment(db)
        self.load_must_deploy_component_instances()
        self.load_cumulative_node_resources()
        self.load_comparative_node_resource()
        self.load_cumulative_component_requirements()
        self.load_comparative_component_requirements()
        #self.load_component_utilization()              # Load C/T of each component instance for RMS constraint.
        #self.load_node_reliability()
        #self.load_comparative_resource_reliability()

    # This function adds communicates constraint for component instance dependencies.
    def add_dependency_constraints(self, solver):
        dependencies = self.componentInstanceDependencies.items()
        for dependency in dependencies:
            if len(dependency[1]) > 0:
                for dependencySource in dependency[1]:
                    srcCompIndex = self.componentInstName2Index[dependencySource]
                    destCompIndex = self.componentInstName2Index[dependency[0]]
                    solver.solver.add(solver.Communicates(srcCompIndex, destCompIndex))

    # This function adds node, process, and component failures as constraints to the given solver.
    def add_failure_constraints(self, solver):
        # Get component, process, and node failures.
        #componentFailures = self.get_failed_components()
        #processFailures = self.get_failed_processes()
        nodeFailures = self.get_failed_nodes()

        # Add above obtained failures.
        #for compFailure in componentFailures:
        #    solver.ComponentFailsOnNode(compFailure[0], compFailure[1])

        #for processFailure in processFailures:
        #    solver.ActorFails(processFailure[0], processFailure[1])

        for nodeFailure in nodeFailures:
            solver.NodeFails(nodeFailure)

    # This function finds component instance that provides a given functionality instance.
    def find_component_instance(self, functionalityInstance):
        for componentInstance in self.componentInstances:
            if componentInstance.functionalityInstanceName == functionalityInstance:
                return componentInstance.name

        return None

    # This function adds replication constraints to the given solver.
    def add_replication_constraints(self, solver):
        for constraint in self.functionalityConstraints:
            constraintToAdd = None
            if constraint[0] == "distribute":
                compIndexes = list()
                for functionalityInstance in constraint[1]:
                    componentInstanceName = self.find_component_instance(functionalityInstance)
                    compIndexes.append(self.componentInstName2Index[componentInstanceName])
                constraintToAdd = solver.DistributeComponents(compIndexes)
            elif constraint[0] == "implies":
                leftComponentInstanceName = self.find_component_instance(constraint[1])
                rightComponentInstanceName = self.find_component_instance(constraint[2])
                rightList = list()
                rightList.append(self.componentInstName2Index[rightComponentInstanceName])
                constraintToAdd = solver.ImpliesOr(self.componentInstName2Index[leftComponentInstanceName],
                                                        rightList)
            elif constraint[0] == "assign":
                componentInstanceName = self.find_component_instance(constraint[1])
                constraintToAdd = solver.Assign(self.componentInstName2Index[componentInstanceName],
                                                self.nodeName2Index[constraint[2]])
            elif constraint[0] == "collocate":
                firstComponentInstanceName = self.find_component_instance(constraint[1])
                secondComponentInstanceName = self.find_component_instance(constraint[2])
                constraintToAdd = solver.CollocateComponents(self.componentInstName2Index[firstComponentInstanceName],
                                                             self.componentInstName2Index[secondComponentInstanceName])
            elif constraint[0] == "atleast":
                compIndexes = list()
                for functionalityInstance in constraint[3]:
                    componentInstanceName = self.find_component_instance(functionalityInstance)
                    componentInstanceIndex = self.componentInstName2Index[componentInstanceName]
                    compIndexes.append(componentInstanceIndex)

                # Check if the atleast group has been previously deployed or not. If it has then we will apply the
                # atleast constraint, if not then this implies initial deployment of the group and therefore we apply
                # maximum optimization.
                prevDeployed = False
                for compIndex in compIndexes:
                    for node in self.nodes:
                        nodeIndex = self.nodeName2Index[node.name]
                        if self.c2n[compIndex][nodeIndex] == 1:
                            prevDeployed = True
                            break

                if prevDeployed:
                    logger.info ("** Previously deployed so using atleast")
                    # This atleast group has been previously deployed so using atleast constraint.
                    objectiveIndex = self.objectiveName2Index[constraint[4]]
                    constraintToAdd = solver.ForceAtleast(objectiveIndex, compIndexes, constraint[1])
                else:
                    #print "** No previous deployedment so using maximum"
                    # This atleast group has not been deployed before so using maximum optimization.
                    #solver.Maximize(compIndexes)
                    logger.info ("** No previous deployment so assigning must deploy")
                    objectiveIndex = self.objectiveName2Index[constraint[4]]
                    constraintToAdd = solver.ForceExactly(objectiveIndex, compIndexes, constraint[2])
                    
                    
            if constraintToAdd is not None:
                solver.solver.add(constraintToAdd)

    # This function returns a list of pair (component index, node index) to represent failed components.
    def get_failed_components(self):
        retval = list()
        for compInst in self.componentInstances:
            if compInst.status == "FAULTY":
                compIndex = self.componentInstName2Index[compInst.name]
                procIndex = self.componentInstIndex2ProcessIndex[compIndex]
                nodeIndex = self.processIndex2NodeIndex[procIndex]

                retval.append((compIndex, nodeIndex))

        return retval

    # This function returns a list of pair (process index, node index) to represent failued processes.
    def get_failed_processes(self):
        retval = list()

        for node in self.nodes:
            for process in node.processes:
                if process.status == "FAULTY":
                    processIndex = self.processName2Index[process.name]
                    nodeIndex = self.processIndex2NodeIndex[processIndex]
                    retval.append((processIndex, nodeIndex))

        return retval

    # This function returns a list of index of nodes that failed.
    def get_failed_nodes(self):
        retval = list()

        for node in self.nodes:
            if node.status == "FAULTY":
                retval.append(self.nodeName2Index[node.name])

        return retval

    # This function dumps generated component instances to the database in ComponentInstances collection.
    # NOTE: This function should be called after load_state so that required component instances information
    #       has been generated.
    def dump_component_instances(self, db):
        # Database collection to update.
        ciColl = db["ComponentInstances"]

        for componentInstance in self.componentInstances:
            componentInstanceDocument = dict()
            componentInstanceDocument["name"] = componentInstance.name
            componentInstanceDocument["type"] = componentInstance.type
            # If status is FAULTY then it means that the component instance is now invalid since it
            # could not be re-deployed.
            #if componentInstance.status == "FAULTY":
            #    componentInstanceDocument["status"] = "INVALID"
            #else:
            #    componentInstanceDocument["status"] = componentInstance.status
            componentInstanceDocument["status"] = componentInstance.status
            componentInstanceDocument["functionalityInstanceName"] = componentInstance.functionalityInstanceName
            componentInstanceDocument["alwaysDeployOnNode"] = componentInstance.alwaysDeployOnNode
            componentInstanceDocument["mustDeploy"] = componentInstance.mustDeploy

            ciColl.update({"name":componentInstance.name},
                          componentInstanceDocument,
                          upsert = True)

    # This function returns a list containing lists of component instances belonging to a same process.
    #
    # NOTE: This function is used by addActorConstraints in ConfigurationSolver to make sure that components
    # of same process is deployed on same node. However, this wont be used for now as our current implementation
    # assumes that each component instance is in its own process.
    def convert_processes(self):
        retval = list()
        for node in self.nodes:
            for process in node.processes:
                comps = list()
                for componentInstance in process.componentInstances:
                    comps.append(self.componentInstName2Index[componentInstance.name])
                retval.append(comps)
        return retval

    # This function stores cumulative (memory or storage) node resources in a R x N matrix where R is the
    # number of different types of cumulative resources and N is the number of nodes.
    #
    # NOTE: Current implementation is limited to just memory and does not consider storage.
    def load_cumulative_node_resources(self):
        # NOTE: For resource related matrices we do not check if node is alive because if a node is
        # not alive nothing will be deployed on that node.
        for node in self.nodes:
            # The compute_cumulative_provisions only returns memory provision.
            nodeResources = node.compute_cumulative_provisions(self.nodeTemplates)

            for resource in nodeResources:
                if resource[0] not in self.cumResource2nodeIndex:
                    self.cumResource2nodeIndex[resource[0]] = list()

                self.cumResource2nodeIndex[resource[0]].append((self.nodeName2Index[node.name],
                                                           resource[1]))

        # Initialize resource to node mapping with 0's to begin with.
        self.nodeCumProvidedResources = [[0 for x in range(len(self.nodes))]
                                         for x in range (len(self.cumResource2nodeIndex))]

        import operator
        # Store sorted list.
        sorted_names = sorted(self.cumResource2nodeIndex.items(), key = operator.itemgetter(0))

        # Fill resource to node mapping (R x N matrix).
        for i in range (len(sorted_names)):
            for valueList in sorted_names[i][1]:
                self.nodeCumProvidedResources[i][valueList[0]] = int(valueList[1])

    # This function stores comparative (devices or artifacts) node resources in a R x N matrix where R
    # is the number of different types of comparative resources and N is the number of nodes.
    #
    # NOTE: Current implementation is limited to just device and does not consider artifacts.
    def load_comparative_node_resource(self):
        for node in self.nodes:
            nodeDeviceResources = node.compute_device_provisions(self.nodeTemplates)

            for deviceResource in nodeDeviceResources:
                if deviceResource.name not in self.compResource2nodeIndex:
                    self.compResource2nodeIndex[deviceResource.name] = list()

                self.compResource2nodeIndex[deviceResource.name].append(self.nodeName2Index[node.name])

        # Initialize resource to node mapping with 0's to begin with.
        self.nodeCompProvidedResources = [[0 for x in range(len(self.nodes))]
                                          for x in range (len(self.compResource2nodeIndex))]

        import operator
        # Store sorted list.
        sorted_names = sorted(self.compResource2nodeIndex.items(), key = operator.itemgetter(0))

        # Fill resource to node mapping (R x N matrix).
        for i in range (len(sorted_names)):
            for nodeIndex in sorted_names[i][1]:
                self.nodeCompProvidedResources[i][nodeIndex] = 1

    # This function computes and stores list of component instance utilization (C/T, i.e, deadline/period).
    def load_component_utilization(self):
        utilization2componentInstIndex = list()
        for componentInstance in self.componentInstances:
            for componentType in self.componentTypes:
                if componentInstance.type == componentType.name:
                    utilization = componentType.deadline[0]/componentType.period[0]
                    utilization2componentInstIndex.append((self.componentInstName2Index[componentInstance.name],
                                                           utilization))

        # Initialize list of utilization to component instance mapping with 0's to begin with.
        self.componentInstUtilization = [0 for x in range (len(self.componentInstances))]

        import operator
        # Store sorted list.
        sorted_names = utilization2componentInstIndex.sort(key = operator.itemgetter(0))

        # Fill utilization to component instance mapping (list of utilization for different component instances).
        for i in range (len(sorted_names)):
            self.componentInstUtilization[i] = sorted_names[i][1] * 100 # Store utilization as percentage.

    # This function computes and stores list of node reliability (exp(-TCritical/MTTF)).
    #
    # NOTE: Currently we only consider a single goal. We assume that the default unit of all time is months.
    def load_node_reliability(self):
        reliability2nodeIndex = list()

        goalTimeElapsed = datetime.datetime.now() - self.goalDescriptions[0].startTime
        avgDaysPerMonth = 30.42
        goalTimeElapsedInMonths = float(goalTimeElapsed.days)/avgDaysPerMonth

        # Compute reliability of each node if elapsed goal time hasn't surpassed expected goal lifetime.
        if goalTimeElapsedInMonths < self.goalDescriptions[0].lifeTime[0]:
            tCritical = self.goalDescriptions[0].lifeTime[0] - goalTimeElapsedInMonths
            from math import exp
            for node in self.nodes:
                reliability = exp(-tCritical/node.meanTimeToFailure[0])
                reliability2nodeIndex.append((self.nodeName2Index[node.name], reliability))
        # If elapsed goal time has surpassed expected goal lifetime, set reliability to maximum (i.e., 1).
        else:
            for node in self.nodes:
                reliability2nodeIndex.append((self.nodeName2Index[node.name], 1))

        # Initialize list of reliability to node mapping with 0's to begin with.
        self.nodeReliability = [0 for x in range (len(self.nodes))]

        import operator
        # Store sorted list.
        sorted_names = sorted(reliability2nodeIndex, key = operator.itemgetter(0))

        # Fill reliability to node mapping (list of reliability for different nodes).
        for i in range (len(sorted_names)):
            self.nodeReliability[i] = sorted_names[i][1]

    # This function computes and stores comparative resource reliability (exp(-TCritical/MTTF)) as elements
    # of R x N matrix where R is the number of different types of comparative resources and N is the number
    # of nodes.
    #
    # NOTE: Devices are the only comparative resources for which reliability is relevant. As such, we only
    # consider devices.
    def load_comparative_resource_reliability(self):
        reliability2compResourceIndex = dict()

        goalTimeElapsed = datetime.datetime.now() - self.goalDescriptions[0].startTime
        avgDaysPerMonth = 30.42
        goalTimeElapsedInMonths = float(goalTimeElapsed.days) / avgDaysPerMonth

        # Compute reliability of each comparative resource if elapsed goal time hasn't surpassed expected
        # goal lifetime.
        if goalTimeElapsedInMonths < self.goalDescriptions[0].lifeTime[0]:
            tCritical = self.goalDescriptions[0].lifeTime[0] - goalTimeElapsedInMonths
            from math import exp
            for node in self.nodes:
                # Store ALL devices.
                nodeDeviceResources = node.compute_device_provisions(self.nodeTemplates)

                for deviceResource in nodeDeviceResources:
                    if deviceResource.name not in reliability2compResourceIndex:
                        reliability2compResourceIndex[deviceResource.name] = list()

                    reliability = exp(-tCritical / deviceResource.meanTimeToFailure[0])
                    reliability2compResourceIndex[deviceResource.name].append((self.nodeName2Index[node.name],
                                                                               reliability))
        else:
            # If elapsed goal time has surpassed expected goal lifetime, set reliability to maximum (i.e., 1).
            for node in self.nodes:
                nodeDeviceResources = node.compute_device_provisions(self.nodeTemplates)
                for deviceResource in nodeDeviceResources:
                    reliability2compResourceIndex[deviceResource.name].append((self.nodeName2Index[node.name],
                                                                               1))

        # Initialize reliability to comparative resource mapping with 0's to begin with.
        self.compResourceReliability = [[0 for x in range (len(self.nodes))]
                                        for x in range (len(reliability2compResourceIndex))]

        import operator
        # Store sorted list.
        sorted_names = sorted(reliability2compResourceIndex.items(), key = operator.itemgetter(0))

        # Fill reliability mapping.
        for i in range (len(sorted_names)):
            for reliability_value in sorted_names[i][1]:    # Each reliability_value is a pair (node index, reliability).
                                                            # This represents reliability of comparative resource (i.e.,
                                                            # device) with index i on node with index node index.
                self.compResourceReliability[i][reliability_value[0]] = reliability_value[1]

    # This function stores cumulative (memory or storage) component requirements in a R x C matrix where R
    # is the number of different types of cumulative resources and C is the number of component instances.
    #
    # NOTE: Current implementation is limited to just memory and does not consider storage.
    def load_cumulative_component_requirements(self):
        for componentInstance in self.componentInstances:
            for componentType in self.componentTypes:
                if componentInstance.type == componentType.name:
                    if "memory" not in self.cumResource2componentInstIndex:
                        self.cumResource2componentInstIndex["memory"] = list()

                    self.cumResource2componentInstIndex["memory"].\
                        append((self.componentInstName2Index[componentInstance.name],
                                componentType.requiredMemory[0]))

        # Initialize resource to component instance mapping with 0's to begin with.
        self.componentInstCumRequiredResources = [[0 for x in range (len(self.componentInstances))]
                                                  for x in range (len(self.cumResource2componentInstIndex))]

        import operator
        # Store sorted list.
        sorted_names = sorted(self.cumResource2componentInstIndex.items(), key = operator.itemgetter(0))

        # Fill resource to component instance mapping (R x C matrix).
        for i in range (len(sorted_names)):
            for valueList in sorted_names[i][1]:
                self.componentInstCumRequiredResources[i][valueList[0]] = int(valueList[1])

        # At this point, check if any required cumulative resources (memory) are missing in provided resources
        # (nodeCumProvidedResources) matrix. If so, add those resources to the aforementioned matrix and fill the
        # corresponding row with 0's
        if (len(self.cumResource2nodeIndex) < len(self.cumResource2componentInstIndex)):
            self.update_cumulative_node_resources()

    # This function updates provided cumulative resources (nodeCumProvidedResources) matrix with required resources
    # that are missing in the provided matrix.
    def update_cumulative_node_resources(self):
        resourcesToAdd = list()
        for requiredResource in self.cumResource2componentInstIndex:
            found = False
            for providedResource in self.cumResource2nodeIndex:
                if requiredResource == providedResource:
                    found = True
                    break
            if not found:
                resourcesToAdd.append(requiredResource)

        for resourceToAdd in resourcesToAdd:
            self.cumResource2nodeIndex[resourceToAdd] = list()

        # Initialize resource to node mapping with 0's to begin with.
        self.nodeCumProvidedResources = [[0 for x in range(len(self.nodes))]
                                         for x in range (len(self.cumResource2nodeIndex))]

        sorted_dict = sorted(self.cumResource2nodeIndex.items(), key = operator.itemgetter(0))

        # Fill resource to node mapping (R x N matrix) again.
        for i in range (len(sorted_dict)):
            for nodeIndex in sorted_dict[i][1]:
                self.nodeCumProvidedResources[i][nodeIndex] = 1

    # This function stores comparative (device or artifact) component requirements in a R x C matrix where R
    # is the number of different types of comparative resources and C is the number of component instances.
    #
    # NOTE: Current implementation is limited to just devices and does not consider artifacts.
    def load_comparative_component_requirements(self):
        for componentInstance in self.componentInstances:
            for componentType in self.componentTypes:
                if componentInstance.type == componentType.name:
                    for requiredDevice in componentType.requiredDevices:
                        if requiredDevice not in self.compResource2componentInstIndex:
                            self.compResource2componentInstIndex[requiredDevice] = list()

                        self.compResource2componentInstIndex[requiredDevice].\
                            append(self.componentInstName2Index[componentInstance.name])

        # Initialize resource to component instance mapping with 0's to begin with.
        self.componentInstCompRequiredResources = [[0 for x in range (len(self.componentInstances))]
                                                   for x in range (len(self.compResource2componentInstIndex))]

        import operator
        # Store sorted list.
        sorted_names = sorted(self.compResource2componentInstIndex.items(), key = operator.itemgetter(0))

        # Fill resource to component instance mapping (R x C matrix).
        for i in range (len(sorted_names)):
            for componentIndex in sorted_names[i][1]:
                self.componentInstCompRequiredResources[i][componentIndex] = 1

        # At this point, check if any required comparative resources (device) are missing in provided resources
        # (nodeCompProvidedResources) matrix. If so, add those devices to the aforementioned matrix and fill the
        # corresponding row with 0's
        if (len(self.compResource2nodeIndex) < len(self.compResource2componentInstIndex)):
            self.update_comparative_node_resources()

        # Also check if any provided comparative resources (device) is missing in required resources
        # (componentInstCompRequiredResources). If so, add those devices and fill corresponding row with 0's.
        if (len(self.compResource2nodeIndex) > len(self.compResource2componentInstIndex)):
            self.update_comparative_component_requirements()


    # This function updates provided comparative resource (nodeCompProvidedResources) matrix with required
    # resources that are missing in the provided matrix.
    def update_comparative_node_resources(self):
        resourcesToAdd = list()
        for requiredResource in self.compResource2componentInstIndex:
            found = False
            for providedResource in self.compResource2nodeIndex:
                if requiredResource == providedResource:
                    found = True
                    break
            if not found:
                resourcesToAdd.append(requiredResource)

        for resourceToAdd in resourcesToAdd:
            self.compResource2nodeIndex[resourceToAdd] = list()

        # Initialize resource to node mapping with 0's to begin with.
        self.nodeCompProvidedResources = [[0 for x in range(len(self.nodes))]
                                          for x in range (len(self.compResource2nodeIndex))]

        sorted_dict = sorted(self.compResource2nodeIndex.items(), key = operator.itemgetter(0))

        # Fill resource to node mapping (R x N matrix) again.
        for i in range (len(sorted_dict)):
            for nodeIndex in sorted_dict[i][1]:
                self.nodeCompProvidedResources[i][nodeIndex] = 1

    # This function updates required comparative resource (componentInstCompRequiredResources) matrix with
    # provided resources that are missing.
    def update_comparative_component_requirements(self):
        resourcesToAdd = list()
        for providedResource in self.compResource2nodeIndex:
            found = False
            for requiredResource in self.compResource2componentInstIndex:
                if providedResource == requiredResource:
                    found = True
                    break
            if not found:
                resourcesToAdd.append(providedResource)

        for resourceToAdd in resourcesToAdd:
            self.compResource2componentInstIndex[resourceToAdd] = list()

        # Initialize resource to component instance mapping with 0's to begin with.
        self.componentInstCompRequiredResources = [[0 for x in range (len(self.componentInstances))]
                                                   for x in range (len(self.compResource2componentInstIndex))]

        sorted_dict = sorted(self.compResource2componentInstIndex.items(), key = operator.itemgetter(0))

        # Fill resource to component instance mapping (R x N) again.
        for i in range (len(sorted_dict)):
            for componentIndex in sorted_dict[i][1]:
                self.componentInstCompRequiredResources[i][componentIndex] = 1

    # This function fills the c2n matrix with appropriate information. If any deployment instruction
    # given then those will be reflected with 1 in the matrix, if not then the matrix will have 0s.
    def load_component_to_node_assignment(self, db):
        logger.info ("Loading component_to_node assignment from db")

        # Initialize c2n matrix with 0s.
        self.c2n = [[0 for x in range(len(self.nodes))]
                    for x in range(len(self.componentInstances))]

        # Cache node name to index.
        for i in range(len(self.nodes)):
            self.nodeName2Index[self.nodes[i].name] = i

        # Cache process name to index.
        i = 0
        for node in self.nodes:
            for process in node.processes:
                self.processName2Index[process.name] = i
                i += 1

        # Cache component instances name to index.
        for i in range(len(self.componentInstances)):
            self.componentInstName2Index[self.componentInstances[i].name] = i

        for node in self.nodes:
            nodeIndex = self.nodeName2Index[node.name]
            if (node.status == "ACTIVE"):
                for process in node.processes:
                    processIndex = self.processName2Index[process.name]
                    for componentInstance in process.componentInstances:
                        componentInstIndex = self.componentInstName2Index[componentInstance.name]
                        self.c2n[componentInstIndex][nodeIndex] = 1
                        self.componentInstIndex2ProcessIndex[componentInstIndex] = processIndex
                        self.processIndex2NodeIndex[processIndex] = nodeIndex

    def load_must_deploy_component_instances(self):
        for compInst in self.componentInstances:
            if compInst.mustDeploy:
                self.mustDeployComponentInstancesIndex.append(self.componentInstName2Index[compInst.name])

    def load_component_types(self, db):
        collection = db["ComponentTypes"]

        for ct in collection.find():
            componentType = Serialize(**ct)
            logger.info ("Adding Component Type with name: " + componentType.name)
            componentTypeToAdd = ComponentType()
            componentTypeToAdd.name = componentType.name
            componentTypeToAdd.providedFunctionality = componentType.providedFunctionality

            requiredMemory = Serialize(**componentType.requiredMemory)
            componentTypeToAdd.requiredMemory = (requiredMemory.memory, requiredMemory.unit)

            requiredStorage = Serialize(**componentType.requiredStorage)
            componentTypeToAdd.requiredStorage = (requiredStorage.storage, requiredStorage.unit)

            componentTypeToAdd.requiredOS = componentType.requiredOS

            for ra in componentType.requiredArtifacts:
                componentTypeToAdd.requiredArtifacts.append(ra)

            for rd in componentType.requiredDevices:
                componentTypeToAdd.requiredDevices.append(rd)

            componentTypeToAdd.startScript = componentType.startScript
            componentTypeToAdd.stopScript = componentType.stopScript

            period = Serialize(**componentType.period)
            componentTypeToAdd.period = (period.time, period.unit)

            deadline = Serialize(**componentType.deadline)
            componentTypeToAdd.deadline = (deadline.time, deadline.unit)

            self.componentTypes.append(componentTypeToAdd)

    def load_node_templates(self, db):
        collection = db["NodeCategories"]

        for nc in collection.find():
            nodeCategory = Serialize(**nc)
            for nt in nodeCategory.nodeTemplates:
                nodeTemplate = Serialize(**nt)
                logger.info ("Adding NodeTemplate with name: " + nodeTemplate.name)
                nodeTemplateToAdd = NodeTemplate()
                nodeTemplateToAdd.name = nodeTemplate.name
                nodeTemplateToAdd.nodeCategory = nodeCategory.name
                nodeTemplateToAdd.availableMemory = \
                    (nodeTemplate.availableMemory["memory"], nodeTemplate.availableMemory["unit"])
                nodeTemplateToAdd.availableStorage = \
                    (nodeTemplate.availableStorage["storage"], nodeTemplate.availableStorage["unit"])
                nodeTemplateToAdd.os = nodeTemplate.OS
                nodeTemplateToAdd.middleware = nodeTemplate.middleware

                for a in nodeTemplate.artifacts:
                    nodeTemplateToAdd.artifacts.append((a["name"], a["location"]))

                for d in nodeTemplate.devices:
                    device = Serialize(**d)
                    deviceToAdd = Device()
                    deviceToAdd.name = device.name

                    for a in device.artifacts:
                        deviceToAdd.artifacts.append((a["name"], a["location"]))

                    deviceToAdd.status = device.status

                    nodeTemplateToAdd.devices.append(deviceToAdd)

                self.nodeTemplates.append(nodeTemplateToAdd)

    # This function loads nodes, processes and component instances.
    def load_nodes_info(self, db):
        collection = db["Nodes"]

        for n in collection.find():
            node = Serialize(**n)
            logger.info ("Adding Node with name: " + node.name)
            nodeToAdd = Node()
            nodeToAdd.name = node.name
            nodeToAdd.nodeTemplate = node.nodeTemplate
            nodeToAdd.status = node.status

            # Add processes if exists.
            if len(node.processes) > 0:
                for p in node.processes:
                    process = Serialize(**p)
                    logger.info ("Adding Process with name: " + process.name)
                    processToAdd = Process()
                    processToAdd.name = process.name
                    processToAdd.pid = process.pid
                    processToAdd.status = process.status

                    # Add component instances if exists.
                    if len(process.components) > 0:
                        for c in process.components:
                            componentInstance = Serialize(**c)
                            logger.info ("Adding Component with name: " + componentInstance.name)
                            componentInstanceToAdd = ComponentInstance()
                            componentInstanceToAdd.name = componentInstance.name
                            componentInstanceToAdd.status = componentInstance.status
                            componentInstanceToAdd.type = componentInstance.type
                            componentInstanceToAdd.functionalityInstanceName = componentInstance.functionalityInstanceName
                            componentInstanceToAdd.alwaysDeployOnNode = componentInstance.alwaysDeployOnNode
                            componentInstanceToAdd.mustDeploy = componentInstance.mustDeploy

                            processToAdd.componentInstances.append(componentInstanceToAdd)
                            self.add_component_instance(componentInstanceToAdd, True)

                    nodeToAdd.processes.append(processToAdd)
            self.nodes.append(nodeToAdd)
        # Sort nodes by names so that node indexes are consistent.
        self.nodes = sorted(self.nodes, key = attrgetter("name"))

    def load_goal_descriptions(self, db):
        collection = db["GoalDescriptions"]

        for gd in collection.find():
            goalDescription = Serialize(**gd)
            logger.info ("Adding GoalDescription with name: " + goalDescription.name)
            goalDescriptionToAdd = GoalDescription()
            goalDescriptionToAdd.name = goalDescription.name

            # Add constraints.
            for rc in goalDescription.replicationConstraints:
                replConstraint = Serialize(**rc)
                replConstraintToAdd = ReplicationConstraint()
                replConstraintToAdd.kind = replConstraint.kind
                replConstraintToAdd.functionality = replConstraint.functionality
                replConstraintToAdd.minInstances = replConstraint.minInstances
                replConstraintToAdd.maxInstances = replConstraint.maxInstances
                replConstraintToAdd.numInstances = replConstraint.numInstances
                replConstraintToAdd.serviceComponentType = replConstraint.serviceComponentType

                for nc in replConstraint.nodeCategories:
                    replConstraintToAdd.nodeCategories.append(nc)

                goalDescriptionToAdd.replicationConstraints.append(replConstraintToAdd)

            # Add objectives.
            for o in goalDescription.objectives:
                objective = Serialize(**o)
                objectiveToAdd = Objective()
                objectiveToAdd.name = objective.name

                # Store functionalities.
                for f in objective.functionalities:
                    functionality = Serialize(**f)
                    functionalityToAdd = Functionality()
                    functionalityToAdd.name = functionality.name

                    for do in functionality.dependsOn:
                        functionalityToAdd.dependsOn.append(do)

                    objectiveToAdd.functionalities.append(functionalityToAdd)

                goalDescriptionToAdd.objectives.append(objectiveToAdd)

            # Compute/generate different entities.
            goalDescriptionToAdd.compute_functionality_instances(self.nodes, self.nodeTemplates)
            goalDescriptionToAdd.compute_component_instances(self.componentTypes)

            # Compute dependencies between component instances.
            goalDescriptionToAdd.compute_component_instance_dependencies()

            # Retrieve and store objectives.
            for objective in goalDescriptionToAdd.get_objectives():
                self.objectives.append(objective)

            # Sort above objectives and store name to ID mapping.
            self.objectives = sorted(self.objectives, key = attrgetter("name"))
            for i in range (len(self.objectives)):
                self.objectiveName2Index[self.objectives[i].name] = i

            # Retrieve and store functionality instances.
            for functionalityInstance in goalDescriptionToAdd.get_functionality_instances():
                self.functionalityInstances.append(functionalityInstance)

            # Get functionality constraints. These will be used to construct constraints for the solver.
            for functionalityConstraint in goalDescriptionToAdd.get_functionality_constraints():
                self.functionalityConstraints.append(functionalityConstraint)

            # Retrieve and store component instances.
            for componentInstance in goalDescriptionToAdd.get_component_instances():
                self.add_component_instance(componentInstance, False)

            # Sort above component instances using name.
            self.componentInstances = sorted(self.componentInstances, key = attrgetter("name"))

            # Retrieve and store dependencies between component instances.
            self.componentInstanceDependencies = \
                copy.deepcopy(goalDescriptionToAdd.get_component_instance_dependencies())

            # Add goal description to collection.
            self.goalDescriptions.append(goalDescriptionToAdd)

            logger.debug ("=====OBJECTIVES=====")
            for i in self.objectives:
                logger.debug (i.name)
            
            logger.debug ("=====FUNCTIONALITY INSTANCES=====")
            for i in self.functionalityInstances:
                logger.debug (i.name + "(" + i.functionalityName + "," + i.objectiveName + ")")
            
            logger.debug ("=====FUNCTIONALITY CONSTRANTS=====")
            for i in self.functionalityConstraints:
                logger.debug (i)
            
            logger.debug ("=====COMPONENT INSTANCES=====")
            for i in self.componentInstances:
                logger.debug (i.name + "(" + i.type + "," + i.functionalityInstanceName + ")")

    # This function loads existing component instances from MongoDB.
    def load_component_instances(self, db):
        collection = db["ComponentInstances"]

        for ci in collection.find():
            componentInstance = Serialize(**ci)

            componentInstanceToAdd = ComponentInstance()
            componentInstanceToAdd.name = componentInstance.name
            componentInstanceToAdd.type = componentInstance.type
            componentInstanceToAdd.status = componentInstance.status    # Status is stored in this collection purely
                                                                        # for display, so we do not read it as status
                                                                        # is only relevant if read from Nodes.
            componentInstanceToAdd.functionalityInstanceName = componentInstance.functionalityInstanceName
            componentInstanceToAdd.alwaysDeployOnNode = componentInstance.alwaysDeployOnNode
            componentInstanceToAdd.mustDeploy = componentInstance.mustDeploy

            # Load node-specific component instances (i.e. component instance that are part of per node replication
            # pattern) if and only if their corresponding node is active.
            if componentInstanceToAdd.alwaysDeployOnNode!= "":
                if(self.check_node_status(componentInstance.alwaysDeployOnNode) == "ACTIVE"):
                    self.add_component_instance(componentInstanceToAdd, False)
                else:
                    logger.info ("Skipping node specific ComponentInstance with name: " + componentInstance.name + " as its assigned node: " + componentInstance.alwaysDeployOnNode + " is not ACTIVE")
            else:
                self.add_component_instance(componentInstanceToAdd, False)

        # Sort component instances by name for consistency.
        self.componentInstances = sorted(self.componentInstances, key = attrgetter("name"))

    # This function checks if a node is currently ACTIVE.
    def check_node_status(self, nodeNameToCheck):
        for node in self.nodes:
            if node.name == nodeNameToCheck:
                return node.status

        return None
