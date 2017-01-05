__author__ = "Subhav Pradhan, Tihamer Levendovszky"
# Base class file for all solvers. General encoding.

from z3 import *
from logger import get_logger

logger = get_logger("configuration_solver")

class ConfigurationSolver(object):


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
        self.NO_OF_NODES = NO_OF_NODES # No of hardware nodes
        self.NO_OF_COMPONENTS = NO_OF_COMPONENTS # No of component >>implementations<< ordered by their >>definitions<<
        self.NO_OF_FUNCTIONS = NO_OF_FUNCTIONS # No of function implementations (if the same service is offered more times, it counts as 2)

        self.mustDeployComponentInstancesIndex = mustDeployComponentInstancesIndex

        # --- The following weights are integers ---
        self.nodeResourceWeights = nodeResourceWeights  # Performance weights for nodes (cumulative)
        self.componentResourceWeights = componentResourceWeights  # Performance weights for components (cumulative)
        self.nodeComparativeWeights = nodeComparativeWeights # Comparative weights for nodes
        self.componentComparativeWeights = componentComparativeWeights  # Comparative weights for components
        self.componentUtilization = componentUtilization
        self.nodeReliability = nodeReliability
        self.compResourceReliability = compResourceReliability
        self.reliabilityThreshold = reliabilityThreshold

        self.actors = actors

        # Performance weights requirements for component interactions -- 1 by default:
        # Backward compatibility for the hand-generated examples
        if communicationWeights is not None:
            self.communicationWeights = communicationWeights
        else:
            self.communicationWeights = [[1]*NO_OF_COMPONENTS for _ in range(NO_OF_COMPONENTS)]

        if links is not None:
            self.links = links
        else:
            self.links = [[1]*NO_OF_NODES for _ in range(NO_OF_NODES)]


        # Initialization -- general
        #self.solver = Optimize()
        self.solver = Solver()
        self.defineComponent2NodeMatrix()
        self.defineResourceConstraints()
        self.defineFunctions()
        #self.addActorConstraints()

        # Initialization -- user defined
        self.addComponentToNodeConstraints()
        self.addComponent2ComponentDependencies()
        self.addFunctionConstraints()

        # Must be last
        #self.solver.push()
        #self.addInteractionConstraints()

    ############## Initializing data structures and setting up the initial constraint environment ##############


    # Defines tha Component instance to Node matrix, and sets up the following constraints:
    # (i) The matrix elements are zero or one; (ii) A component instance can belong to only one node.
    # (iii) The sum of resource weights of the components deployed on a node cannot exceed the resource weight of the
    # node; (iv) Total resilience of a configuration (product of each component's resilience) should be greater
    # that the goal's resilience threshold.
    def defineComponent2NodeMatrix(self):
        # Component-Node matrix
        # If component i uses node j, c2n_i_j is true; false otherwise
        self.c2n = [ [ Int("c2n_%s_%s" % (i, j)) for j in range(self.NO_OF_NODES) ]
            for i in range(self.NO_OF_COMPONENTS) ]

        c2n = self.c2n

        # Range constraints: zero or one
        val_c2n = [ Or(c2n[i][j]==0,c2n[i][j]==1) for j in range(self.NO_OF_NODES)
          for i in range(self.NO_OF_COMPONENTS)]

        # General assignment constraint to ensure each component is only deployed in a single
        # node, or not deployed at all.
        g_assignment_c2n = [  Sum([c2n[i][j] for j in range(self.NO_OF_NODES)]) <= 1
            for i in range(self.NO_OF_COMPONENTS)]

        # Must deploy assignment constraint for mustDeploy component instances. This ensures that
        # a single instance of these component instances are always present.
        md_assignment_c2n = [  Sum([c2n[i][j] for j in range(self.NO_OF_NODES)]) == 1
            for i in self.mustDeployComponentInstancesIndex]

        # Adding constraints to the solver
        self.solver.add(val_c2n + g_assignment_c2n + md_assignment_c2n)

    # Resource constraints
    def defineResourceConstraints(self):
        perf_c2n = [self.nodeResourceWeights[k][j] >= Sum([self.c2n[i][j]*self.componentResourceWeights[k][i]
            for i in range(self.NO_OF_COMPONENTS)])
                for j in range(self.NO_OF_NODES)
                    for k in range (len(self.nodeResourceWeights))]

        com_const = []
        if self.componentComparativeWeights is not None and self.nodeComparativeWeights is not None:
            com_const = [Implies(self.Assigned(i,j),self.nodeComparativeWeights[k][j] >= self.componentComparativeWeights[k][i]) for i in range(self.NO_OF_COMPONENTS)
                    for j in range(self.NO_OF_NODES)
                        for k in range (len(self.nodeComparativeWeights))]

        # Rate Monotonic Scheduling constraint.
        #rms_c2n = [69 >= Sum([c2n[i][j]*self.componentUtilization[i]
        #    for i in range(self.NO_OF_COMPONENTS)])
        #        for j in range (self.NO_OF_NODES)]

        #Reliability constraints.
        #rel_const = [ Product([ Sum([c2n[i][j]*self.nodeReliability[j]*
        #                            Product([ c2n[i][j] * self.componentComparativeWeights[k][i]*
        #                                      self.nodeComparativeWeights[k][j]*
        #                                      self.compResourceReliability[k][j]
        #                                      for k in range (len(self.componentComparativeWeights))])
        #                            for j in range(self.NO_OF_NODES)])
        #                        for i in range(self.NO_OF_COMPONENTS)]) >= self.reliabilityThreshold]

        self.solver.add(perf_c2n + com_const)
        #self.solver.add(val_c2n + assignment_c2n + perf_c2n + com_const + rel_const)
        #self.solver.add(val_c2n + assignment_c2n + perf_c2n + com_const + rms_c2n)

    # Defines all the function variables. Additional user constraints are defined in addFunctionConstraints().
    def defineFunctions(self):
        self.f = [ Bool("f_%s" % i)   for i in range(self.NO_OF_FUNCTIONS) ]
        self.solver.add(self.f)
        for f in self.f:
            self.solver.add(f==True)

    # Adds the actor constraint: the component instances belonging to the same actor must be assigned to the same node.
    def addActorConstraints(self):
        c2n = self.c2n
        # Actor constraints: components belonging to the same actor should be located on the same node
        act_c2n2d =[self.Equals([c2n[compIx][n] for compIx in actor]) for n in range(self.NO_OF_NODES) for actor in self.actors]
        act_c2n = [val for subl in act_c2n2d for val in subl] # Flattening the list

        # Adding constraint to the solver
        self.solver.add(act_c2n)

    # Certain constraints cannot be provided by Z3 independent data structures. These constraints are incorporated
    # in the derived class.

    def addComponentToNodeConstraints(self):
        raise NotImplementedError, "This functions must be overridden in the derived class"


    # To be overridden
    def addComponent2ComponentDependencies(self):
        raise NotImplementedError, "This functions must be overridden in the derived class"


    # To be overridden
    def addInteractionConstraints(self):
        raise NotImplementedError, "This functions must be overridden in the derived class"

    # To be overridden
    def addFunctionConstraints(self):
        raise NotImplementedError, "This functions must be overridden in the derived class"


    ########################### Resilience Verification Primitives ######################

    # Input: a list of Z3 variables;
    # Output: constraint set that equals all the variables in chain
    def Equals(self, vars):
        ret=[]
        for i in range(len(vars)-1):
            ret.append(vars[i]==vars[i+1])
        return ret

    # Input: an index of the component in the component instance node matrix.
    # an index of a node in the component instance node matrix.
    # Output: A constraint that assigns component i to node j
    def Assign(self, i, j):
        return Implies(self.Enabled(i), self.c2n[i][j] ==1)

    # Input: an index of the component in the component instance node matrix.
    # an index of a node in the component instance node matrix.
    # Output: A constraint that returns true if component i is assigned to node j

    def Assigned(self, i, j):
        return self.c2n[i][j] >0

    # Input: an index of the component in the component instance node matrix.
    # an index of a node in the component instance node matrix, and a set of components that are using the resource.
    # Output: A constraint that assigns component c to node n, and collocates the client components with c.

    def TurnIntoBinaryResource(self, c, n, client_components):
        return And(self.Assign(c,n),And([self.CollocateComponents(c, cc) for cc in client_components ]))

    # Input: an index of the component in the component instance node matrix.
    # Output: a boolean expression that is true if the component is assigned to a node; false otherwise
    # The constraint sums the row of the component instance and checks if it is greater than zero.

    def Enabled(self, i):
        return Sum([self.c2n[i][j] for j in range(self.NO_OF_NODES)])>0

    # Input: a pair of component instances
    # Output: an constraint that ensures that the component instances must be assigned to the same node
    def CollocateComponents(self, c1, c2):
        collocation = [self.Equals([self.c2n[c1][n],self.c2n[c2][n]]) for n in range(self.NO_OF_NODES)]
        return  Implies(And(self.Enabled(c1), self.Enabled(c2)), And([val for subl in collocation for val in subl])) # Flattening the list


    # Input: a list of component instances
    # Output: an constraint that ensures that the component instances must be assigned to different nodes
    def DistributeComponents(self, components):
        distribution = [Sum([self.c2n[compIx][n] for compIx in components])<=1 for n in range(self.NO_OF_NODES)]
        return distribution

    # Input: the indices of two components in the component instance to node matrix
    # Output: a constraints that makes sure that there is a link between the nodes
    # the components are deployed on. If the  two components are on the same node
    # the constraint is still satisfied.
    #def Communicates(self, i, j):
    #    c2n = self.c2n
    #    c2l = [ Implies(And(c2n[i][n1]*c2n[j][n2]!=0, n1!=n2), self.links[n1][n2] >=self.communicationWeights[i][j])
    #    for n1 in range(self.NO_OF_NODES) for n2 in range(self.NO_OF_NODES) ]
    #    return c2l
    #    #return And(c2l)

    def Communicates(self, i, j):
        c2n = self.c2n
        c2l = [ Implies(And(c2n[i][n1]*c2n[j][n2]!=0, n1!=n2), self.links[n1][n2] == 1)
            for n1 in range(self.NO_OF_NODES) for n2 in range(self.NO_OF_NODES) ]
        return c2l
        #return And(c2l)

    # Input a component and a list of components
    # Effect A constraint that enforces that the component c1 requires
    # either one of the components in the componentList to be Enabled.
    def ImpliesOr(self, c1, componentList):
        return Implies(self.Enabled(c1),Sum([self.c2n[i][j] for i in componentList for j in range(self.NO_OF_NODES)])>=1)

    # Input: the indices of a function and a list of component indices in the component instance to node matrix; positive
    # integer n
    # Output: a constraints that makes sure that exactly n of the components in the list must be enabled
    # to provide the function.
    def ForceExactly(self, function, componentList, n):
        return Implies(self.f[function],Sum([self.c2n[i][j] for i in componentList for j in range(self.NO_OF_NODES)]) ==n)

    # Input: the indices of a function and a list of component indices in the component instance to node matrix; positive
    # integer n
    # Output: a constraints that makes sure that at least n of the components in the list must be enabled
    # to provide the function.
    def ForceAtleast(self, function, componentList, n):
        return Implies(self.f[function], Sum([self.c2n[i][j] for i in componentList for j in range(self.NO_OF_NODES)]) >=n)

    # Input: the indices of a function and a list of component indices in the component instance to node matrix; positive
    # integer n
    # Output: a constraints that makes sure that at most n of the components in the list must be enabled
    # to provide the function.
    def ForceAtmost(self, function, componentList, n):
        return Implies(self.f[function],Sum([self.c2n[i][j] for i in componentList for j in range(self.NO_OF_NODES)]) <=n)

    def Maximize(self, componentList):
        component_sum = Sum([self.c2n[i][j] for i in componentList for j in range(self.NO_OF_NODES)])
        self.solver.maximize(component_sum)

    ################# Manipulation interface: introducing constraints caused by faults ###################

    # Input: an index of a component in the component instance node matrix.
    # Output: none
    # Adds a constraint that makes sure that the component cannot be assigned to any node.
    def ComponentFails(self, i):
        c2n = self.c2n
        self.solver.add(Sum([c2n[i][n] for n in range(self.NO_OF_NODES)])==0)

    # Input: an index of a component in the component instance node matrix, and the index of a node.
    # Output: none
    # Adds a constraint that makes sure that the component cannot be assigned to the specified node.
    # It models the situation when a component crashes on a specific node.
    def ComponentFailsOnNode(self, c, n):
        c2n = self.c2n
        self.solver.add(c2n[c][n]==0)

    # Input: an index of a component in the component instance node matrix, and the index of a node.
    # Output: none
    # Adds a constraint that makes sure that the component cannot be assigned to the specified node.
    # It models the situation when a component crashes on a specific node.
    #def ComponentFailsOnNode(self, c, n):
    #    c2n = self.c2n
    #    self.solver.add(c2n[c][n]==0)

    # Input: an index of a component in the component instance node matrix, and the index of a node.
    # Output: none
    # Adds a constraint that makes sure that the component cannot be assigned to the specified node.
    # It models the situation when a component crashes on a specific node.
    def ComponentFailsWithActor(self, c, n):
        c2n = self.c2n
        self.solver.add(c2n[c][n]==0)

    # Input: an index of a node in the component instance node matrix.
    # Output: none
    # Adds a constraint that makes sure that no component cannot be assigned to this node.
    def NodeFails(self, i):
        c2n = self.c2n
        self.solver.add(Sum([c2n[c][i] for c in range(self.NO_OF_COMPONENTS)])==0)

    # Input: an index of an actor in the actor to component vector provided at initialization.
    # Output: none
    # Calls self.ComponentFails for each component assigned to this actor
    def ActorFails(self, i, j):
        # We make all the component instances belonging to the actor fail fail
        for ci in self.actors[i]:
            #self.ComponentFails(ci)
            self.ComponentFailsOnNode(ci, j)

    # Input: two indexes in the node to link matrix provided at initialization
    # Output: None
    def LinkFails(self, i, j):
        self.links[i][j]=self.links[j][i] = 0
        self.solver.pop() # Restore state saved in constructor
        self.solver.push()
        self.addInteractionConstraints()



    ############### Computation and analysis ######################################

    # Gets another solution for the c2n matrix
    def solve(self):
        s = self.solver
        if s.check() == sat:
            m = s.model()
            r = [ [ m.evaluate(self.c2n[i][j]) for j in range(self.NO_OF_NODES) ]
              for i in range(self.NO_OF_COMPONENTS) ]
            print_matrix(r)
        else:
            logger.error ("Failed to solve")
            logger.info (s)

    def get_models(self):
        s= self.solver
        result =[]

        s.push() # Save solver state

        while True:
            if s.check() == sat:
                m = s.model()

                result.append(m)
                # Create a new constraint the blocks the current model
                block = []
                for d in m:
                    # d is a declaration
                    if d.arity() > 0:
                        raise Z3Exception("Uninterpreted functions are not supported.")
                    # create a constant from declaration
                    c = d()
                    if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                        raise Z3Exception("Arrays and uninterpreted sorts are not supported.")
                    block.append(c != m[d])
                s.add(Or(block))
            else:
                s.pop() # Restore solver state
                return result


    def number_of_valid_configurations(self):
        ms = self.get_models()
        return len(ms)

    def print_c2n(self, model):
        r = [ [ model.evaluate(self.c2n[i][j]) for j in range(self.NO_OF_NODES) ]
                    for i in range(self.NO_OF_COMPONENTS) ]
        print_matrix(r)

    def get_maximal_model(self):
        s= self.solver


        s.push() # Save solver state

        last_model  = None
        minvalue = 0

        summa = Int("sum")
        sumOfComps =   Sum([self.c2n[i][j] for j in range(self.NO_OF_NODES)
          for i in range(self.NO_OF_COMPONENTS)])


        # Node counters
        nc = [  Int("nc_%s" % i) for i in range(self.NO_OF_NODES) ]
        nc_assignments_1 = [ Implies(Sum([self.c2n[i][j] for i in range(self.NO_OF_COMPONENTS)]) >0, nc[j]==1)   for j in range(self.NO_OF_NODES)]
        nc_assignments_0 = [ Implies(Sum([self.c2n[i][j] for i in range(self.NO_OF_COMPONENTS)]) ==0, nc[j]==0)   for j in range(self.NO_OF_NODES)]

        s.add(nc_assignments_0+nc_assignments_1)

        sumOfNodes = Sum([nc[i] for i in range(self.NO_OF_NODES)])


        # Debug
        # sn =  Int("sn")
        # s.add(sn == sumOfNodes)

        # sumOfNodes2 =  Sum([self.c2n[i][0] for i in range(self.NO_OF_COMPONENTS)])
        #
        # sn2 =  Int("sn2")
        # s.add(sn2 == sumOfNodes2)


        sumOfAll = sumOfComps + sumOfNodes
        s.add(sumOfAll == summa)


        maxvalue = 0

        while True:
            r = s.check()
            if r == unsat:
                if last_model != None:
                    # Debug
                    # print "sn: ",
                    # print last_model[sn]

                    # print "sn2: ",
                    # print last_model[sn2]


                    #print last_model

                    maxvalue = int(str(last_model[summa]))
                    s.pop()
                    return [maxvalue, last_model]
                else:
                    s.pop()
                    return [maxvalue, last_model]
            if r == unknown:
                raise Z3Exception("failed")
            last_model = s.model()

            minvalue = int(str(last_model[summa]))

            s.add(summa > last_model[summa])

        s.pop()
        return [maxvalue, last_model]


    # Helper for distance between adjacency matrices
    def abs(self,x):
            return If(x >= 0,x,-x)
