__author__ = "Tihamer Levendovszky, Subhav Pradhan"


from new_configuration_solver import NewConfigurationSolver


# Backend-aware new configuration solver

class NewConfigurationSolverBound(NewConfigurationSolver):
    def __init__(self, backend):
        #super(NewConfigurationSolverBound, self).__init__(len(backend.nodes), len(backend.components), len(backend.functions),
        #    backend.ncumw, backend.ccumw, backend.ncompw, backend.ccompw, None, backend.convertActors())

        super(NewConfigurationSolverBound, self).__init__(len(backend.nodes),
                                                          len(backend.componentInstances),
                                                          len(backend.objectives),
                                                          backend.mustDeployComponentInstancesIndex,
                                                          backend.nodeCumProvidedResources,
                                                          backend.componentInstCumRequiredResources,
                                                          backend.nodeCompProvidedResources,
                                                          backend.componentInstCompRequiredResources,
                                                          None,
                                                          backend.convert_processes(),
                                                          backend.componentInstUtilization,
                                                          backend.nodeReliability,
                                                          backend.compResourceReliability,
                                                          0)
                                                          #backend.goalDescriptions[0].reliabilityThreshold) # NOTE: See below.

        # NOTE: We currently assume a single goal. This makes no difference (as far as we know) to most of the
        # existing constraints. However, in case of the reliability constraint, different goal can have different
        # reliability threshold! #TODO: Use component instance to goal mapping.

        self.componentNames = list()
        for c in backend.componentInstances:
            self.componentNames.append(c.name)

        self.nodeNames = list()
        for n in backend.nodes:
            self.nodeNames.append(n.name)


    # Names for debugging and pretty printing
    componentNames = None
    nodeNames = None

    # Called from outside
    def ComputeAndSaveSolution(self):
        pass

    def addComponentToNodeConstraints(self):
       pass

    def addComponent2ComponentDependencies(self):
        pass

    # Dummy
    def addInteractionConstraints(self):
        pass

    # Dummy
    def addFunctionConstraints(self):
        pass
