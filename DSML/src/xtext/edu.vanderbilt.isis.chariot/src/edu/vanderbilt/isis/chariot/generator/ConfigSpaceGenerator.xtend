package edu.vanderbilt.isis.chariot.generator

import com.google.common.collect.HashMultimap
import com.google.common.collect.Lists
import com.google.common.collect.Multimap
import com.mongodb.DB
import com.mongodb.Mongo
import com.mongodb.MongoException
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
import org.slf4j.LoggerFactory
import edu.vanderbilt.isis.chariot.chariot.PerNodeReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.GoalDescription
import edu.vanderbilt.isis.chariot.datamodel.GoalDescription.DM_GoalDescription
import edu.vanderbilt.isis.chariot.datamodel.ReplicationConstraintKind

class ConfigSpaceGenerator implements IGenerator {
	//@Inject extension IQualifiedNameProvider
	
	final val LOGGER= LoggerFactory.getLogger(typeof(ConfigSpaceGenerator))
	/*
	 * 
	 */
	override doGenerate(Resource input, IFileSystemAccess fsa){// throws MongoException {
		//throw new UnsupportedOperationException("TODO: auto-generated method stub")
		//var mongo = new Mongo("192.168.1.6")
		//val mongo = new Mongo("127.0.0.1",7777)
		val mongo = new Mongo()
		try {
		  mongo.getConnector().getDBPortPool(mongo.getAddress()).get().ensureOpen();
		} catch (Exception e) {
		  LOGGER.info("Cannot reach MongoDb, ignoring configspace generator");
		  return;
		}
		
		try {
			// Get database.
			val db = mongo.getDB('ConfigSpace') 
			
			// Call get status to check remote connection. This will throw MongoException is
			// Mongo server is unreachable.
			db.getStats()
			
			if ((input.allContents.toIterable.filter(ExternalComponent)).size() > 0) {
				generateExternalComponents (input.allContents.toIterable.filter(ExternalComponent), db)
			}
			if ((input.allContents.toIterable.filter(VoterServiceComponent)).size() > 0) {
				generateVoterServiceComponents (input.allContents.toIterable.filter(VoterServiceComponent), db)
			}
			if ((input.allContents.toIterable.filter(ConsensusServiceComponent)).size() > 0) {
				generateConsensusServiceComponents (input.allContents.toIterable.filter(ConsensusServiceComponent), db)
			}
			if ((input.allContents.toIterable.filter(NodesCategory)).size() > 0) {
				generateNodeCategories (input.allContents.toIterable.filter(NodesCategory), db)
			}
			if ((input.allContents.toIterable.filter(GoalDescription).size() > 0)) {
				generateGoalDescriptions (input.allContents.toIterable.filter(GoalDescription), db)
				
				// Call generate component instances in the solver. This call is placed here for now
				// assuming everything else will be generated before system descriptions.
				//val String[] commands = #[lcmpath, '--java', '--jpath', targetPath, fullname]
				//var runTime = Runtime.getRuntime();
			}
		} catch (MongoException me) {
			LOGGER.error("Caught MongoException. Cannot connect to Mongo server.")
		} catch (Exception e) {
			LOGGER.error("Caught exception: " + e)
			e.printStackTrace()
		} finally {
			mongo.close()
		}
	}
	
	/*
	 * 
	 */
	def generateVoterServiceComponents (Iterable<VoterServiceComponent> voterServiceComponents, DB db) {
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
			
			componentType.insert (db)
		}
	}
	
	/*
	 * 
	 */
	def generateConsensusServiceComponents (Iterable<ConsensusServiceComponent> consensusServiceComponents, DB db) {
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
			
			componentType.insert (db)
		}
	}
	
	
	/*
	 * 
	 */
	def generateExternalComponents (Iterable<ExternalComponent> externalComponents, DB db) {
		// Loop through each external component.
		for (c : externalComponents) {
			var DM_ComponentType componentType = new DM_ComponentType ()

			componentType.init()
			
			// Store name.
			componentType.setName (c.getName())
			
			// Filter and store functionality provision.
			componentType.setProvidedFunctionality (c.parts.filter(ExternalFunctionalityProvision).get(0).getFunctionality().getName())
			
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
			
			componentType.insert (db)
		}
	}
	
	/*
	 * 
	 */
	def generateComponentRequirements (Component c, DM_ComponentType ct) {
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
		if (c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ExternalComponentImpl")) {
			memoryRequirements = Lists.newArrayList ((c as ExternalComponent).parts.filter(MemoryRequirement))
			storageRequirements = Lists.newArrayList ((c as ExternalComponent).parts.filter(StorageRequirement))
			osRequirements = Lists.newArrayList ((c as ExternalComponent).parts.filter(OSRequirement))
			middlewareRequirements = Lists.newArrayList ((c as ExternalComponent).parts.filter(MiddlewareRequirement))
			artifactRequirements = Lists.newArrayList ((c as ExternalComponent).parts.filter(ArtifactRequirement))
			deviceRequirements = Lists.newArrayList ((c as ExternalComponent).parts.filter(DeviceRequirement))
		}
		else if (c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.VoterServiceComponentImpl")) {
			memoryRequirements = Lists.newArrayList ((c as VoterServiceComponent).parts.filter(MemoryRequirement))
			storageRequirements = Lists.newArrayList ((c as VoterServiceComponent).parts.filter(StorageRequirement))
			osRequirements = Lists.newArrayList ((c as VoterServiceComponent).parts.filter(OSRequirement))
			middlewareRequirements = Lists.newArrayList ((c as VoterServiceComponent).parts.filter(MiddlewareRequirement))
			artifactRequirements = Lists.newArrayList ((c as VoterServiceComponent).parts.filter(ArtifactRequirement))
			deviceRequirements = Lists.newArrayList ((c as VoterServiceComponent).parts.filter(DeviceRequirement))
		}
		else if (c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ConsensusServiceComponentImpl")) {
			memoryRequirements = Lists.newArrayList ((c as ConsensusServiceComponent).parts.filter(MemoryRequirement))
			storageRequirements = Lists.newArrayList ((c as ConsensusServiceComponent).parts.filter(StorageRequirement))
			osRequirements = Lists.newArrayList ((c as ConsensusServiceComponent).parts.filter(OSRequirement))
			middlewareRequirements = Lists.newArrayList ((c as ConsensusServiceComponent).parts.filter(MiddlewareRequirement))
			artifactRequirements = Lists.newArrayList ((c as ConsensusServiceComponent).parts.filter(ArtifactRequirement))
			deviceRequirements = Lists.newArrayList ((c as ConsensusServiceComponent).parts.filter(DeviceRequirement))
		}
		
		// Store memory requirements.
		// NOTE: Only first should/will be stored.
		if (memoryRequirements.size() > 0) {
			val memory = memoryRequirements.get(0).getMemory()
			val memUnit = memoryRequirements.get(0).getUnit()
			ct.setRequiredMemory [
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
			ct.setRequiredStorage [
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
				ct.setRequiredOS (SupportedOS.LINUX)
			else if (osRequirement.android)
				ct.setRequiredOS (SupportedOS.ANDROID)
		}
				
		// Store middleware requirement.
		// NOTE: Only first should/will be stored.
		if (middlewareRequirements.size() > 0) {
			var middlewareRequirement = middlewareRequirements.get(0)
			if (middlewareRequirement.rtidds)
				ct.setRequiredMiddleware (SupportedMiddleware.RTIDDS)
			else if (middlewareRequirement.alljoyn)
				ct.setRequiredMiddleware (SupportedMiddleware.ALLJOYN)
			else if (middlewareRequirement.lcm)
				ct.setRequiredMiddleware (SupportedMiddleware.LCM)
		}
		
		// Store artifact requirements.
		// NOTE: Artifacts could be more than one.
		for (a : artifactRequirements)
			ct.addRequiredArtifact (a.getArtifact().getName())
			
		// Store device requirements.
		// NOTE: Devices could be more than one.
		for (d: deviceRequirements)
			ct.addRequiredDevice (d.getDevice().getName())
	}
	
	/*
	 * 
	 */
	def generateNodeCategories (Iterable<NodesCategory> nodeCategories, DB db) {
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
			nodeCategory.insert (db)	
		}
	}
	
	/*
	 * 
	 */
	def generateGoalDescriptions (Iterable<GoalDescription> goalDescriptions, DB db) {
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
			
			goalDescription.insert(db)
		}
	}
	
	/*
	 * 
	 */
	def Multimap<String, String> getFunctionalities (Composition c) {
		var Multimap<String, String> retval = HashMultimap.create()
		for (fe : c.getFunctionedges()) {
			var toFunctionality = 
				findFunctionalityWithInput (fe.getToPort().getName(), fe.eResource.allContents.toIterable.filter(Functionality))
			var fromFunctionality = 
				findFunctionalityWithOutput (fe.getFromPort().getName(), fe.eResource.allContents.toIterable.filter(Functionality))
						
			retval.put(toFunctionality, fromFunctionality)
		}
		return retval
	}
	
	/*
	 * 
	 */
	def String findFunctionalityWithInput (String functionalityParam, Iterable<Functionality> functionalities) {
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
	 * 
	 */
	def String findFunctionalityWithOutput (String functionalityParam, Iterable<Functionality> functionalities) {
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