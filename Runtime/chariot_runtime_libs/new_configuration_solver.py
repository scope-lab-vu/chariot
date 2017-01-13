__author__ = "Tihamer Levendovszky, Subhav Pradhan"
# Base class for solvers computing new configuration

from z3 import *
from configuration_solver import ConfigurationSolver
from logger import get_logger

logger = get_logger("new_configuration_solver")

class NewConfigurationSolver(ConfigurationSolver):

    def __init__(self,
                 NO_OF_NODES,
                 NO_OF_COMPONENTS,
                 NO_OF_FUNCTIONS,
                 mustDeployComponentInstancesIndex,
                 nodeResourceWeights,
                 componentResourceWeights,
                 nodeComparativeWeights,
                 componentComparativeWeights,
                 links,
                 actors,
                 componentUtilization,
                 nodeReliability,
                 compResourceReliability,
                 reliabilityThreshold,
                 communicationWeights=None):
        super(NewConfigurationSolver, self).__init__(NO_OF_NODES,
                                                     NO_OF_COMPONENTS,
                                                     NO_OF_FUNCTIONS,
                                                     mustDeployComponentInstancesIndex,
                                                     nodeResourceWeights,
                                                     componentResourceWeights,
                                                     nodeComparativeWeights,
                                                     componentComparativeWeights,
                                                     links,
                                                     actors,
                                                     componentUtilization,
                                                     nodeReliability,
                                                     compResourceReliability,
                                                     reliabilityThreshold,
                                                     communicationWeights)

        self.c2n_old = None # Baseline adjacency matrix (initial model)
        self.nodeNames =None # Names for printing, logging, and debugging
        self.nodeNames =None # Names for printing, logging, and debugging
        self.componentNames = None # Names for printing, logging, and debugging

    # Prints the differences between the initial and the new configuration
    # For logging and debugging
    def print_difference(self, componentsToShutDown, componentsToStart):
        logger.info ("Printing differences:")
        for component in componentsToStart:
            logger.info ("START Component %s on Node %s." % (self.componentNames[component[0]], self.nodeNames[component[1]]))

        for component in componentsToShutDown:
            logger.info ("SHUTDOWN Component %s on Node %s." % (self.componentNames[component[0]], self.nodeNames[component[1]]))

    # 1. Computes the new configuration
    # 2. Retrieves the difference between the initial and the new configuration along with the distance between the
    # old and new configuration
    def get_difference(self, initial):
        componentsToStart = []
        componentsToShutDown = []

        [dist, model] = self.get_next_configuration(initial)

        if model is None: # No solution
            return [None, None, None, None]

        logger.info ("New configuration was found. Distance from previous config: %d" % dist)
        for i in range(self.NO_OF_COMPONENTS):
            for j in range(self.NO_OF_NODES):
                element = model[self.c2n[i][j]].as_long()
                element_old = self.c2n_old[i][j]

                if element_old < element:
                    componentsToStart.append([i,j]) # Start ci on ni
                if element_old > element:
                    componentsToShutDown.append([i,j]) # Stop ci on ni

        return [componentsToShutDown, componentsToStart, model, dist]

    # Retrieves the closest valid configuration to the original configuration
    def get_next_configuration(self, initial):
        s= self.solver
        s.push() # Save solver state
        logger.info ("Stats: " + str(s.statistics()))
        logger.info ("Number of assertions: " + str(len(s.assertions())))

        # Here, c2n is a list of Z3 int variables that will be assigned values by the solver.
        # c2n_old is a CxN matrix of integers that represents CURRENT (will be 0's during initial deployment)
        # component-to-node mapping.
        c2n = self.c2n
        c2n_old = self.c2n_old

        #if not initial:
        #    config_distance = Sum([self.abs(c2n_old[i][j] - c2n[i][j]) for j in range(self.NO_OF_NODES)
        #        for i in range(self.NO_OF_COMPONENTS)])
        #    config_distance_val = Int("config_distance_val")
        #    s.minimize(config_distance)
        #    s.add(config_distance_val == config_distance)

        #r = s.check()
        #if r == unsat:
        #    return [None, None]
        #elif r == sat:
        #    if initial:
        #        return [self.NO_OF_COMPONENTS, s.model()]
        #    else:
        #        return [s.model()[config_distance_val].as_long(), s.model()]
        #else:
        #    raise Z3Exception("Failed.")

        absNorm = Int("absNorm")

        absNormFormula = Sum([self.abs(c2n_old[i][j] - c2n[i][j]) for j in range(self.NO_OF_NODES)
            for i in range(self.NO_OF_COMPONENTS)])

        s.add(absNorm == absNormFormula)

        last_model = None
        count = 0
        while True:
            count += 1
            r = s.check()
            if r == unsat:
                s.pop()
                if last_model is None:
                    return [None, None]
                else:
                    logger.info ("Number of least dist iteration: " + str(count))
                    return [last_model[absNorm].as_long(), last_model]

            elif r == unknown:
                raise Z3Exception("Failed.")

            else:
                last_model = s.model()
                s.add(absNorm < last_model[absNorm])

    # Check if current state (represented by c2n_old) is valid.
    def check_valid(self):
        s = self.solver

        # Save solver state.
        s.push()

        # Counter to keep track of the number of constraints we add.
        count = 0

        # Add constraints to reflect current c2n mapping.
        for i in range(self.NO_OF_COMPONENTS):
            for j in range(self.NO_OF_NODES):
                if (self.c2n_old[i][j] == 1):
                    s.add(self.c2n[i][j] == 1)
                    count += 1

        # Check if satisfiable.
        r = s.check()
        if (r == sat):
            logger.info ("** CURRENT IS VALID. NO RECONF REQUIRED.")
            logger.info (s.model())
            return True
        else:
            return False
