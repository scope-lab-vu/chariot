__author__ = 'Tihamer Levendovszky'


from NewConfigurationSolver import NewConfigurationSolver


# Backend-aware new configuration solver

class NewConfigurationSolverBound(NewConfigurationSolver):
    def __init__(self, backend):
        #super(NewConfigurationSolverBound, self).__init__(len(backend.nodes), len(backend.components), len(backend.functions),
        #    backend.ncumw, backend.ccumw, backend.ncompw, backend.ccompw, None, backend.convertActors())

        super(NewConfigurationSolverBound, self).__init__(len(backend.nodes),
                                                          len(backend.componentInstances),
                                                          len(backend.objectiveInstances),
                                                          backend.nodeCumProvidedResources,
                                                          backend.componentInstCumRequiredResources,
                                                          backend.nodeCompProvidedResources,
                                                          backend.componentInstCompRequiredResources,
                                                          None,
                                                          backend.convert_processes(),
                                                          backend.componentInstUtilization,
                                                          backend.nodeReliability,
                                                          backend.compResourceReliability,
                                                          backend.systemDescriptions[0].reliabilityThreshold) # NOTE: See below.

        # NOTE: We currently assume a single system. This makes no difference (as far as we know) to most of the
        # existing constraints. However, in case of the reliability constraint, different systems can have different
        # reliability threshold! #TODO: Use component instance to system mapping.

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