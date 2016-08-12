package edu.vanderbilt.isis.chariot.generator

import com.google.common.collect.HashMultimap
import com.google.common.collect.Lists
import com.google.common.collect.Multimap
import com.mongodb.DB
import com.mongodb.Mongo
import edu.vanderbilt.isis.chariot.chariot.ActiveReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.Artifact
import edu.vanderbilt.isis.chariot.chariot.ArtifactRequirement
import edu.vanderbilt.isis.chariot.chariot.Component
import edu.vanderbilt.isis.chariot.chariot.ComponentDeadline
import edu.vanderbilt.isis.chariot.chariot.ComponentPeriod
import edu.vanderbilt.isis.chariot.chariot.Composition
import edu.vanderbilt.isis.chariot.chariot.ConsensusReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.ConsensusServiceComponent
import edu.vanderbilt.isis.chariot.chariot.DeviceRequirement
import edu.vanderbilt.isis.chariot.chariot.DeviceSupported
import edu.vanderbilt.isis.chariot.chariot.ExternalComponent
import edu.vanderbilt.isis.chariot.chariot.ExternalFunctionalityProvision
import edu.vanderbilt.isis.chariot.chariot.Functionality
import edu.vanderbilt.isis.chariot.chariot.MemoryProvision
import edu.vanderbilt.isis.chariot.chariot.MemoryRequirement
import edu.vanderbilt.isis.chariot.chariot.Middleware
import edu.vanderbilt.isis.chariot.chariot.MiddlewareRequirement
import edu.vanderbilt.isis.chariot.chariot.NodesCategory
import edu.vanderbilt.isis.chariot.chariot.OSRequirement
import edu.vanderbilt.isis.chariot.chariot.OSSupported
import edu.vanderbilt.isis.chariot.chariot.StartScript
import edu.vanderbilt.isis.chariot.chariot.StopScript
import edu.vanderbilt.isis.chariot.chariot.StorageProvision
import edu.vanderbilt.isis.chariot.chariot.StorageRequirement
import edu.vanderbilt.isis.chariot.chariot.VoterReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.VoterServiceComponent
import edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_ComponentType
import edu.vanderbilt.isis.chariot.datamodel.MemoryUnit
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_NodeCategory
import edu.vanderbilt.isis.chariot.datamodel.Status
import edu.vanderbilt.isis.chariot.datamodel.StorageUnit
import edu.vanderbilt.isis.chariot.datamodel.SupportedMiddleware
import edu.vanderbilt.isis.chariot.datamodel.SupportedOS
import edu.vanderbilt.isis.chariot.datamodel.TimeUnit
import java.util.ArrayList
import org.eclipse.emf.ecore.resource.Resource
import org.eclipse.xtext.generator.IFileSystemAccess
import org.eclipse.xtext.generator.IGenerator
import edu.vanderbilt.isis.chariot.chariot.PerNodeReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.GoalDescription
import edu.vanderbilt.isis.chariot.datamodel.GoalDescription.DM_GoalDescription
import edu.vanderbilt.isis.chariot.datamodel.ReplicationConstraintKind
import java.util.logging.Logger

class ConfigSpaceGenerator implements IGenerator {
	//@Inject extension IQualifiedNameProvider
	
	// Declaring class variables.
	public static val Logger LOGGER = Logger.getLogger("ChariotGenerator")
	private var String mongoAddr
	private var int mongoPortNum
	private var Mongo mongoClient
	private var DB db
	
	/*
	 * Constructor.
	 */
	new() {
		// Get mongoDB server IP address and port from predefined environment variables.
		this.mongoAddr = System.getenv("MONGO_ADDRESS")
		var String mongoPort = System.getenv("MONGO_PORT")
		
		if (this.mongoAddr == null || this.mongoAddr == "localhost")
			this.mongoAddr = "127.0.0.1"

		if (mongoPort == null)
			this.mongoPortNum = 27017
		else
			this.mongoPortNum = Integer.parseInt(mongoPort)
		
		this.mongoClient = new Mongo(this.mongoAddr, this.mongoPortNum)
		
		// Check mongoDB server connection.
		try {
			this.mongoClient.getConnector().getDBPortPool(this.mongoClient.getAddress()).get().ensureOpen();
		} catch (Exception e) {
			LOGGER.severe("Cannot reach MongoDb server at: " + mongoAddr + ", ignoring configuration space generator");
			this.mongoClient.close()
		 	return;
		}
		
		// Get configuration space database.
		this.db = this.mongoClient.getDB('ConfigSpace') 
	}
	
	/*
	 * Method that performs configuration space generation.
	 * 
	 * @param input	Input resource on which generation must be performed.
	 * @param fsa	File system accessor.
	 */
	override doGenerate(Resource input, IFileSystemAccess fsa){
		//throw new UnsupportedOperationException("TODO: auto-generated method stub")

		// Generate various design-time system description artifacts.
		if ((input.allContents.toIterable.filter(ExternalComponent)).size() > 0)
			generateExternalComponents (input.allContents.toIterable.filter(ExternalComponent))
		
		if ((input.allContents.toIterable.filter(VoterServiceComponent)).size() > 0)
			generateVoterServiceComponents (input.allContents.toIterable.filter(VoterServiceComponent))
			
		if ((input.allContents.toIterable.filter(ConsensusServiceComponent)).size() > 0)
			generateConsensusServiceComponents (input.allContents.toIterable.filter(ConsensusServiceComponent))

		if ((input.allContents.toIterable.filter(NodesCategory)).size() > 0)
			generateNodeCategories (input.allContents.toIterable.filter(NodesCategory))
			
		if ((input.allContents.toIterable.filter(GoalDescription).size() > 0))
			generateGoalDescriptions (input.allContents.toIterable.filter(GoalDescription))
	}
	
	/*
	 * Method to generate voter service components.
	 * 
	 * @param voterServiceComponents	List of voter service components in a model resource.
	 */
	def generateVoterServiceComponents (Iterable<VoterServiceComponent> voterServiceComponents) {
		// Loop through each voter service component.
		for (c : voterServiceComponents) {
			var DM_ComponentType componentType = new DM_ComponentType ()
			
			componentType.init ()
			
			// Store name.
			componentType.setName (c.getName())
		
			// NOTE: Unlike external component types, voter service component types will not have
			// any associated provided functionality.
			
			// Store component requirements.
			generateComponentRequirements (c, componentType)

			// Filter and store start script.
			if (c.parts.filter(StartScript).size() > 0)
				componentType.setStartScript(c.parts.filter(StartScript).get(0).getScript())
			
			// Filter and store stop script.
			if (c.parts.filter(StopScript).size() > 0)
				componentType.setStopScript(c.parts.filter(StopScript).get(0).getScript())
			
			// Filter and store period and deadline.
			if (c.parts.filter(ComponentPeriod).size() > 0) {
				componentType.setPeriod [
					var period = c.parts.filter(ComponentPeriod).get(0).getPeriod()
					var unit = c.parts.filter(ComponentPeriod).get(0).getUnit()
					setTime (period)
					if (unit.months)
						setUnit (TimeUnit.MONTHS)
					else if (unit.days)
						setUnit (TimeUnit.DAYS)
					else if (unit.seconds)
						setUnit (TimeUnit.SECONDS)
					else if (unit.milliseconds)
						setUnit (TimeUnit.MILLISECONDS)
					else if (unit.microseconds)
						setUnit (TimeUnit.MICROSECONDS)
				]
			}
			
			if (c.parts.filter(ComponentDeadline).size() > 0) {
				componentType.setDeadline [
					var deadline = c.parts.filter(ComponentDeadline).get(0).getDeadline()
					var unit = c.parts.filter(ComponentDeadline).get(0).getUnit()
					setTime (deadline)
					if (unit.months)
						setUnit (TimeUnit.MONTHS)
					else if (unit.days)
						setUnit (TimeUnit.DAYS)
					else if (unit.seconds)
						setUnit (TimeUnit.SECONDS)
					else if (unit.milliseconds)
						setUnit (TimeUnit.MILLISECONDS)
					else if (unit.microseconds)
						setUnit (TimeUnit.MICROSECONDS)
				]
			}
			
			componentType.insert (this.db)
		}
	}
	
	/*
	 * Method to generate consensus service components.
	 * 
	 * @param consensusServiceComponents	List of consensus service components in a model resource.
	 */
	def generateConsensusServiceComponents (Iterable<ConsensusServiceComponent> consensusServiceComponents) {
		// Loop through each consensus service component.
		for (c : consensusServiceComponents) {
			var DM_ComponentType componentType = new DM_ComponentType ()
			
			componentType.init ()
			
			// Store name.
			componentType.setName (c.getName())
		
			// NOTE: Unlike external component types, consensus service component types will not have
			// any associated provided functionality.
			
			// Store component requirements.
			generateComponentRequirements (c, componentType)

			// Filter and store start script.
			if (c.parts.filter(StartScript).size() > 0)
				componentType.setStartScript(c.parts.filter(StartScript).get(0).getScript())
			
			// Filter and store stop script.
			if (c.parts.filter(StopScript).size() > 0)
				componentType.setStopScript(c.parts.filter(StopScript).get(0).getScript())
			
			// Filter and store period and deadline.
			if (c.parts.filter(ComponentPeriod).size() > 0) {
				componentType.setPeriod [
					var period = c.parts.filter(ComponentPeriod).get(0).getPeriod()
					var unit = c.parts.filter(ComponentPeriod).get(0).getUnit()
					setTime (period)
					if (unit.months)
						setUnit (TimeUnit.MONTHS)
					else if (unit.days)
						setUnit (TimeUnit.DAYS)
					else if (unit.seconds)
						setUnit (TimeUnit.SECONDS)
					else if (unit.milliseconds)
						setUnit (TimeUnit.MILLISECONDS)
					else if (unit.microseconds)
						setUnit (TimeUnit.MICROSECONDS)
				]
			}
			
			if (c.parts.filter(ComponentDeadline).size() > 0) {
				componentType.setDeadline [
					var deadline = c.parts.filter(ComponentDeadline).get(0).getDeadline()
					var unit = c.parts.filter(ComponentDeadline).get(0).getUnit()
					setTime (deadline)
					if (unit.months)
						setUnit (TimeUnit.MONTHS)
					else if (unit.days)
						setUnit (TimeUnit.DAYS)
					else if (unit.seconds)
						setUnit (TimeUnit.SECONDS)
					else if (unit.milliseconds)
						setUnit (TimeUnit.MILLISECONDS)
					else if (unit.microseconds)
						setUnit (TimeUnit.MICROSECONDS)
				]
			}
			
			componentType.insert (this.db)
		}
	}
	
	
	/*
	 * Method to generate external components.
	 * 
	 * @param externalComponents	List of external components in a model resource.
	 */
	def generateExternalComponents (Iterable<ExternalComponent> externalComponents) {
		// Loop through each external component.
		for (c : externalComponents) {
			var DM_ComponentType componentType = new DM_ComponentType ()

			componentType.init()
			
			// Store name.
			componentType.setName (c.getName())
			
			// Filter and store functionality provision.
			componentType.setProvidedFunctionality (c.parts.filter(ExternalFunctionalityProvision).
														get(0).getFunctionality().getName())
			
			// Store component requirements.
			generateComponentRequirements (c, componentType)

			// Filter and store start script.
			if (c.parts.filter(StartScript).size() > 0)
				componentType.setStartScript(c.parts.filter(StartScript).get(0).getScript())
			
			// Filter and store stop script.
			if (c.parts.filter(StopScript).size() > 0)
				componentType.setStopScript(c.parts.filter(StopScript).get(0).getScript())
			
			// Filter and store period and deadline.
			if (c.parts.filter(ComponentPeriod).size() > 0) {
				componentType.setPeriod [
					var period = c.parts.filter(ComponentPeriod).get(0).getPeriod()
					var unit = c.parts.filter(ComponentPeriod).get(0).getUnit()
					setTime (period)
					if (unit.months)
						setUnit (TimeUnit.MONTHS)
					else if (unit.days)
						setUnit (TimeUnit.DAYS)
					else if (unit.seconds)
						setUnit (TimeUnit.SECONDS)
					else if (unit.milliseconds)
						setUnit (TimeUnit.MILLISECONDS)
					else if (unit.microseconds)
						setUnit (TimeUnit.MICROSECONDS)
				]
			}
			
			if (c.parts.filter(ComponentDeadline).size() > 0) {
				componentType.setDeadline [
					var deadline = c.parts.filter(ComponentDeadline).get(0).getDeadline()
					var unit = c.parts.filter(ComponentDeadline).get(0).getUnit()
					setTime (deadline)
					if (unit.months)
						setUnit (TimeUnit.MONTHS)
					else if (unit.days)
						setUnit (TimeUnit.DAYS)
					else if (unit.seconds)
						setUnit (TimeUnit.SECONDS)
					else if (unit.milliseconds)
						setUnit (TimeUnit.MILLISECONDS)
					else if (unit.microseconds)
						setUnit (TimeUnit.MICROSECONDS)
				]
			}
			
			componentType.insert (this.db)
		}
	}
	
	/*
	 * Method to generate requirements of a component.
	 * 
	 * @param comp		Component for which requirements must be generated.
	 * @param compBean	Mongo bean corresponding to the component for which requirements
	 * 					must be generated.	
	 */
	def generateComponentRequirements (Component comp, DM_ComponentType compBean) {
		var ArrayList<MemoryRequirement> memoryRequirements
		var ArrayList<StorageRequirement> storageRequirements
		var ArrayList<OSRequirement> osRequirements
		var ArrayList<MiddlewareRequirement> middlewareRequirements
		var ArrayList<ArtifactRequirement> artifactRequirements
		var ArrayList<DeviceRequirement> deviceRequirements
		
		//Filter for different requirements.
		/*if (c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ChariotComponentImpl")) {
			memoryRequirements =
				Lists.newArrayList ((c as ChariotComponent).parts.filter(MemoryRequirement))
			storageRequirements =
				Lists.newArrayList ((c as ChariotComponent).parts.filter(StorageRequirement))
			osRequirements =
				Lists.newArrayList ((c as ChariotComponent).parts.filter(OSRequirement))
			middlewareRequirements =
				Lists.newArrayList ((c as ChariotComponent).parts.filter(MiddlewareRequirement))
			artifactRequirements = 
				Lists.newArrayList ((c as ChariotComponent).parts.filter(ArtifactRequirement))
			deviceRequirements =
				Lists.newArrayList ((c as ChariotComponent).parts.filter(DeviceRequirement))
		}
		else*/ 
		if (comp.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ExternalComponentImpl")) {
			memoryRequirements = Lists.newArrayList ((comp as ExternalComponent).parts.filter(MemoryRequirement))
			storageRequirements = Lists.newArrayList ((comp as ExternalComponent).parts.filter(StorageRequirement))
			osRequirements = Lists.newArrayList ((comp as ExternalComponent).parts.filter(OSRequirement))
			middlewareRequirements = Lists.newArrayList ((comp as ExternalComponent).parts.filter(MiddlewareRequirement))
			artifactRequirements = Lists.newArrayList ((comp as ExternalComponent).parts.filter(ArtifactRequirement))
			deviceRequirements = Lists.newArrayList ((comp as ExternalComponent).parts.filter(DeviceRequirement))
		}
		else if (comp.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.VoterServiceComponentImpl")) {
			memoryRequirements = Lists.newArrayList ((comp as VoterServiceComponent).parts.filter(MemoryRequirement))
			storageRequirements = Lists.newArrayList ((comp as VoterServiceComponent).parts.filter(StorageRequirement))
			osRequirements = Lists.newArrayList ((comp as VoterServiceComponent).parts.filter(OSRequirement))
			middlewareRequirements = Lists.newArrayList ((comp as VoterServiceComponent).parts.filter(MiddlewareRequirement))
			artifactRequirements = Lists.newArrayList ((comp as VoterServiceComponent).parts.filter(ArtifactRequirement))
			deviceRequirements = Lists.newArrayList ((comp as VoterServiceComponent).parts.filter(DeviceRequirement))
		}
		else if (comp.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ConsensusServiceComponentImpl")) {
			memoryRequirements = Lists.newArrayList ((comp as ConsensusServiceComponent).parts.filter(MemoryRequirement))
			storageRequirements = Lists.newArrayList ((comp as ConsensusServiceComponent).parts.filter(StorageRequirement))
			osRequirements = Lists.newArrayList ((comp as ConsensusServiceComponent).parts.filter(OSRequirement))
			middlewareRequirements = Lists.newArrayList ((comp as ConsensusServiceComponent).parts.filter(MiddlewareRequirement))
			artifactRequirements = Lists.newArrayList ((comp as ConsensusServiceComponent).parts.filter(ArtifactRequirement))
			deviceRequirements = Lists.newArrayList ((comp as ConsensusServiceComponent).parts.filter(DeviceRequirement))
		}
		
		// Store memory requirements.
		// NOTE: Only first should/will be stored.
		if (memoryRequirements.size() > 0) {
			val memory = memoryRequirements.get(0).getMemory()
			val memUnit = memoryRequirements.get(0).getUnit()
			compBean.setRequiredMemory [
				setMemory (memory)
				if (memUnit.gb)
					setUnit (MemoryUnit::GB)
				else if (memUnit.mb)
					setUnit (MemoryUnit::MB)
				else if (memUnit.kb)
					setUnit (MemoryUnit::KB)
			]
		}
		
		// Store storage requirements.
		// NOTE: Only first should/will be stored.
		if (storageRequirements.size() > 0) {
			val storage = storageRequirements.get(0).getStorage()
			val storageUnit = storageRequirements.get(0).getUnit()
			compBean.setRequiredStorage [
				setStorage (storage)
				if (storageUnit.gb)
					setUnit (StorageUnit::GB)
				else if (storageUnit.mb)
					setUnit (StorageUnit::MB)
				else if (storageUnit.kb)
					setUnit (StorageUnit::KB)
			]
		}
			
		// Store OS requirement.
		// NOTE: Only first should/will be stored.
		if (osRequirements.size() > 0) {
			var osRequirement = osRequirements.get(0)
			if (osRequirement.linux)
				compBean.setRequiredOS (SupportedOS.LINUX)
			else if (osRequirement.android)
				compBean.setRequiredOS (SupportedOS.ANDROID)
		}
				
		// Store middleware requirement.
		// NOTE: Only first should/will be stored.
		if (middlewareRequirements.size() > 0) {
			var middlewareRequirement = middlewareRequirements.get(0)
			if (middlewareRequirement.rtidds)
				compBean.setRequiredMiddleware (SupportedMiddleware.RTIDDS)
			else if (middlewareRequirement.alljoyn)
				compBean.setRequiredMiddleware (SupportedMiddleware.ALLJOYN)
			else if (middlewareRequirement.lcm)
				compBean.setRequiredMiddleware (SupportedMiddleware.LCM)
		}
		
		// Store artifact requirements.
		// NOTE: Artifacts could be more than one.
		for (a : artifactRequirements)
			compBean.addRequiredArtifact (a.getArtifact().getName())
			
		// Store device requirements.
		// NOTE: Devices could be more than one.
		for (d: deviceRequirements)
			compBean.addRequiredDevice (d.getDevice().getName())
	}
	
	/*
	 * Method to generate node categories.
	 * 
	 * @param nodeCategories	List of node categories in a model resource.
	 */
	def generateNodeCategories (Iterable<NodesCategory> nodeCategories) {
		// Loop through each node category.
		for (nc : nodeCategories) {
			var DM_NodeCategory nodeCategory = new DM_NodeCategory()
			
			nodeCategory.init()
			
			// Store name.
			nodeCategory.setName (nc.getName())
			
			// Store templates.
			for (nt : nc.getNodeTemplates()) {
				nodeCategory.addNodeTemplate [
					init()
					setName (nt.getName())
					if (nt.getNodeTemplateInfo().filter(MemoryProvision).size() > 0) {
						val memory = nt.getNodeTemplateInfo().filter(MemoryProvision).get(0).getMemory()
						val unit = nt.getNodeTemplateInfo().filter(MemoryProvision).get(0).getUnit()
						setAvailableMemory [
							setMemory (memory)
							if (unit.gb)
								setUnit (MemoryUnit::GB)
							else if (unit.mb)
								setUnit (MemoryUnit::MB)
							else if (unit.kb)
								setUnit (MemoryUnit::KB)
						]
					}
						
					if (nt.getNodeTemplateInfo().filter(StorageProvision).size() > 0) {
						setAvailableStorage [
							val storage = nt.getNodeTemplateInfo().filter(StorageProvision).get(0).getStorage()
							val unit = nt.getNodeTemplateInfo().filter(StorageProvision).get(0).getUnit()
							setStorage (storage)
							if (unit.gb)
								setUnit (StorageUnit::GB)
							else if (unit.mb)
								setUnit (StorageUnit::MB)
							else if (unit.kb)
								setUnit (StorageUnit::KB)
						]
					}
						
					if (nt.getNodeTemplateInfo().filter(OSSupported).size() > 0) {
						var os = nt.getNodeTemplateInfo().filter(OSSupported).get(0)
						if (os.linux)
							setOS (SupportedOS::LINUX)
						if (os.android)
							setOS (SupportedOS::ANDROID)
					}
						
					if (nt.getNodeTemplateInfo().filter(Middleware).size() > 0) {
						var middlewareList = nt.getNodeTemplateInfo().filter(Middleware).get(0)
						for (m : middlewareList.getMiddleware()) {
							if (m.rtidds)
								setMiddleware (SupportedMiddleware::RTIDDS)
							if (m.alljoyn)
								setMiddleware (SupportedMiddleware::ALLJOYN)
							if (m.lcm)
								setMiddleware (SupportedMiddleware::LCM)
						}
					}
						
					for (a : nt.getNodeTemplateInfo().filter(Artifact)) {
						addArtifact [
							init()
							if (a.jar)
								setName (a.getName() + ".jar")
							if (a.sharedObject)
								setName (a.getName() + ".so")
							setLocation (a.getLocation())
						]
					}
						
					for (d : nt.getNodeTemplateInfo().filter(DeviceSupported)) {
						addDevice [
							init()
							setName (d.getName())
								
							for (a : d.getArtifacts()) {
								addArtifact [
									init()
									if (a.jar)
										setName (a.getName() + ".jar")
									else
										setName (a.getName() + ".so")
									setLocation (a.getLocation())
								]
							}
							setStatus (Status::ACTIVE)
						]
					}
				]
			}
			nodeCategory.insert (this.db)	
		}
	}
	
	/*
	 * Method to generate goal descriptions.
	 * 
	 * @param goalDescriptions	List of goal descriptions in a model resource.
	 */
	def generateGoalDescriptions (Iterable<GoalDescription> goalDescriptions) {
		// Loop through each goal description.
		for (g : goalDescriptions) {
			var DM_GoalDescription goalDescription = new DM_GoalDescription()
			
			goalDescription.init()
			
			// Store name.
			goalDescription.setName (g.getName())
			
			// Store constraints.
			for (c : g.getReplicationConstraints()) {
				goalDescription.addReplicationConstraint [
					init()
					if(c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ConsensusReplicationConstraintImpl")) {
						setKind(ReplicationConstraintKind::CONSENSUS_REPLICATION)
						setFunctionality((c as ConsensusReplicationConstraint).getFunctionality().getName())
						setMinInstances((c as ConsensusReplicationConstraint).getRange().getLower())
						setMaxInstances((c as ConsensusReplicationConstraint).getRange().getUpper())
						setNumInstances((c as ConsensusReplicationConstraint).getRange().getExact())
						setServiceComponentType((c as ConsensusReplicationConstraint).getServiceComponent().getName())
					}
					
					if(c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ActiveReplicationConstraintImpl")) {
						setKind(ReplicationConstraintKind::CLUSTER_REPLICATION)
						setFunctionality((c as ActiveReplicationConstraint).getFunctionality().getName())
						setMinInstances((c as ActiveReplicationConstraint).getRange().getLower())
						setMaxInstances((c as ActiveReplicationConstraint).getRange().getUpper())
						setNumInstances((c as ActiveReplicationConstraint).getRange().getExact())
					}
						
					if(c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.VoterReplicationConstraintImpl")) {
						setKind(ReplicationConstraintKind::VOTER_REPLICATION)
						setFunctionality((c as VoterReplicationConstraint).getFunctionality().getName())
						setMinInstances((c as VoterReplicationConstraint).getRange().getLower())
						setMaxInstances((c as VoterReplicationConstraint).getRange().getUpper())
						setNumInstances((c as VoterReplicationConstraint).getRange().getExact())
						setServiceComponentType((c as VoterReplicationConstraint).getServiceComponent().getName())
					}
					
					if(c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.PerNodeReplicationConstraintImpl")) {
						setKind(ReplicationConstraintKind::PER_NODE_REPLICATION)
						setFunctionality((c as PerNodeReplicationConstraint).getFunctionality().getName())
						for (nodeCategory : (c as PerNodeReplicationConstraint).getCategories())
							addNodeCategory(nodeCategory.getName())
					}
				]
			}
			
			// Store objectives.
			for (o : g.getRequiredobjectives()) {
				goalDescription.addObjective [
					init()
					setName(o.getName())
					
					// Store functionalities in a map where key represents functionalities that
					// have dependencies and corresponding value represents those dependencies.
					val functionalityMap = getFunctionalities (o.getComposition())
					
					// List to keep track of added functionalities.
					var addedFunctionalities = new ArrayList<String>()
					
					// First add keys of the functionalitiyMap. These keys represent functionalities that
					// have dependencies.
					for (f : functionalityMap.keys()) {
						if (!addedFunctionalities.contains(f)) {
							addFunctionality[
								init()
								setName(f)
								for (d : functionalityMap.get(f))
									addDependsOn(d)
							]
							addedFunctionalities.add(f)
						}
					}
					
					// Now add values of the functionalityMap. These values represent functionalities on
					// which other functionalities depend on.
					for (f: functionalityMap.values()) {
						if (!addedFunctionalities.contains(f)) {
							addFunctionality[
								init()
								setName(f)
							]
							addedFunctionalities.add(f)
						}
					}
				]
			}
			
			goalDescription.insert(this.db)
		}
	}
	
	/*
	 * Method to get functionalities associated with a composition.
	 * 
	 * @param composition	Composition for which functionalities must be determined.
	 */
	def Multimap<String, String> getFunctionalities (Composition composition) {
		var Multimap<String, String> retval = HashMultimap.create()
		for (fe : composition.getFunctionedges()) {
			var toFunctionality = 
				findFunctionalityWithInput (fe.getToPort().getName(), 
											fe.eResource.allContents.toIterable.filter(Functionality))
			var fromFunctionality = 
				findFunctionalityWithOutput (fe.getFromPort().getName(), 
											 fe.eResource.allContents.toIterable.filter(Functionality))
						
			retval.put(toFunctionality, fromFunctionality)
		}
		return retval
	}
	
	/*
	 * Method to find functionality with given input parameter.
	 * 
	 * @param functionalityParam	Functionality input parameter to find.
	 * @param functionalities		List of functionalities to search.
	 */
	def String findFunctionalityWithInput (String functionalityParam, 
										   Iterable<Functionality> functionalities) {
		for (f : functionalities) {
			if (f.getInputFunctionalityParam() != null) {
				for (i : f.getInputFunctionalityParam().getInputParams()) {
					if (i.getName().equals(functionalityParam)) 
						return f.getName()
				}
			}
		}
	}
	
	/*
	 * Method to find functionality with given output parameter.
	 * 
	 * @param functionalityParam	Functionality output parameter to find.
	 * @param functionalities		List of functionalities to search.
	 */
	def String findFunctionalityWithOutput (String functionalityParam, 
											Iterable<Functionality> functionalities) {
		for (f : functionalities) {
			if (f.getOutputFunctionalityParam() != null) {
				for (o : f.getOutputFunctionalityParam().getOutputParams()) {
					if (o.getName().equals(functionalityParam))
						return f.getName()
				}
			}
		}
	}
}