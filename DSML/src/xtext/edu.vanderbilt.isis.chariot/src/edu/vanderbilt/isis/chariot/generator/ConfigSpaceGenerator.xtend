package edu.vanderbilt.isis.chariot.generator

import org.eclipse.xtext.generator.IGenerator
import org.eclipse.emf.ecore.resource.Resource
import org.eclipse.xtext.generator.IFileSystemAccess
//import com.google.inject.Inject
//import org.eclipse.xtext.naming.IQualifiedNameProvider
import com.mongodb.Mongo
import com.mongodb.DB
import java.util.ArrayList
import com.google.common.collect.Lists
import edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_ComponentType
import edu.vanderbilt.isis.chariot.datamodel.MemoryUnit
import edu.vanderbilt.isis.chariot.datamodel.StorageUnit
import edu.vanderbilt.isis.chariot.chariot.MemoryRequirement
import edu.vanderbilt.isis.chariot.chariot.StorageRequirement
import edu.vanderbilt.isis.chariot.chariot.OSRequirement
import edu.vanderbilt.isis.chariot.datamodel.SupportedOS
import edu.vanderbilt.isis.chariot.chariot.MiddlewareRequirement
import edu.vanderbilt.isis.chariot.datamodel.SupportedMiddleware
import edu.vanderbilt.isis.chariot.chariot.Component
import edu.vanderbilt.isis.chariot.chariot.ExternalComponent
import edu.vanderbilt.isis.chariot.chariot.ExternalFunctionalityProvision
import edu.vanderbilt.isis.chariot.chariot.NodesCategory
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_NodeCategory
import edu.vanderbilt.isis.chariot.chariot.Node
import edu.vanderbilt.isis.chariot.chariot.NodeCategoryLabel
import edu.vanderbilt.isis.chariot.chariot.MemoryProvision
import edu.vanderbilt.isis.chariot.chariot.StorageProvision
import edu.vanderbilt.isis.chariot.chariot.OSSupported
import edu.vanderbilt.isis.chariot.chariot.Middleware
import edu.vanderbilt.isis.chariot.chariot.NetworkInterface
import edu.vanderbilt.isis.chariot.chariot.Artifact
import edu.vanderbilt.isis.chariot.chariot.DeviceRequirement
import edu.vanderbilt.isis.chariot.chariot.StartScript
import edu.vanderbilt.isis.chariot.chariot.StopScript
import edu.vanderbilt.isis.chariot.chariot.ArtifactRequirement
import edu.vanderbilt.isis.chariot.chariot.NodeTemplate
import edu.vanderbilt.isis.chariot.chariot.DeviceSupported
import edu.vanderbilt.isis.chariot.datamodel.Node.DM_Node
import edu.vanderbilt.isis.chariot.chariot.NodeTemplateLabel
import edu.vanderbilt.isis.chariot.datamodel.Status
import edu.vanderbilt.isis.chariot.chariot.SystemDescription
import edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_SystemDescription
import edu.vanderbilt.isis.chariot.datamodel.SystemConstraintKind
import edu.vanderbilt.isis.chariot.chariot.ConsensusReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.ActiveReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.VoterReplicationConstraint
import edu.vanderbilt.isis.chariot.chariot.Composition
import edu.vanderbilt.isis.chariot.chariot.Functionality
import com.google.common.collect.Multimap
import com.google.common.collect.HashMultimap
import edu.vanderbilt.isis.chariot.chariot.CategoryConstraint
import edu.vanderbilt.isis.chariot.chariot.perNodeFunctionality
import com.mongodb.MongoException
import org.slf4j.LoggerFactory
import edu.vanderbilt.isis.chariot.chariot.ComponentPeriod
import edu.vanderbilt.isis.chariot.chariot.ComponentDeadline
import edu.vanderbilt.isis.chariot.chariot.VoterServiceComponent
import edu.vanderbilt.isis.chariot.chariot.ConsensusServiceComponent
import edu.vanderbilt.isis.chariot.datamodel.TimeUnit

class ConfigSpaceGenerator implements IGenerator {
	//@Inject extension IQualifiedNameProvider
	//@Inject extension CHARIOT_Test t1
	
	
	final val LOGGER= LoggerFactory.getLogger(typeof(ConfigSpaceGenerator))
	/*
	 * 
	 */
	override doGenerate(Resource input, IFileSystemAccess fsa){// throws MongoException {
		//throw new UnsupportedOperationException("TODO: auto-generated method stub")
		//var mongo = new Mongo("192.168.1.6")
		var mongo = new Mongo()
		try {
		  mongo.getConnector().getDBPortPool(mongo.getAddress()).get().ensureOpen();
		} catch (Exception e) {
		  LOGGER.info("Cannot reach MongoDb, ignoring configspace generator");
		  return;
		}
		
		try {
			// Get database.
			var db = mongo.getDB('ConfigSpace') 
			
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
				generateNodeCategories (input.allContents.toIterable.filter(NodesCategory), 
										input.allContents.toIterable.filter(NodeTemplate),
										db)
			}
			if ((input.allContents.toIterable.filter(SystemDescription).size() > 0)) {
				generateSystems (input.allContents.toIterable.filter(SystemDescription), db)
				
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
			val DM_ComponentType componentType = new DM_ComponentType ()
			
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
					val period = c.parts.filter(ComponentPeriod).get(0).getPeriod()
					val unit = c.parts.filter(ComponentPeriod).get(0).getUnit()
					setPeriod (period)
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
					val deadline = c.parts.filter(ComponentDeadline).get(0).getDeadline()
					val unit = c.parts.filter(ComponentDeadline).get(0).getUnit()
					setDeadline (deadline)
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
			val DM_ComponentType componentType = new DM_ComponentType ()
			
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
					val period = c.parts.filter(ComponentPeriod).get(0).getPeriod()
					val unit = c.parts.filter(ComponentPeriod).get(0).getUnit()
					setPeriod (period)
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
					val deadline = c.parts.filter(ComponentDeadline).get(0).getDeadline()
					val unit = c.parts.filter(ComponentDeadline).get(0).getUnit()
					setDeadline (deadline)
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
			val DM_ComponentType componentType = new DM_ComponentType ()

			componentType.init()
			
			// Store name.
			componentType.setName (c.getName())
			
			// Filter for external functionality provisions and store them.
			val externalFunctionalityProvisions = c.parts.filter(ExternalFunctionalityProvision)
			for (f : externalFunctionalityProvisions) {
				componentType.addProvidedFunctionality(f.getFunctionality().getName())
			}
			
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
					val period = c.parts.filter(ComponentPeriod).get(0).getPeriod()
					val unit = c.parts.filter(ComponentPeriod).get(0).getUnit()
					setPeriod (period)
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
					val deadline = c.parts.filter(ComponentDeadline).get(0).getDeadline()
					val unit = c.parts.filter(ComponentDeadline).get(0).getUnit()
					setDeadline (deadline)
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
			ct.setMemoryRequirement [
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
			ct.setStorageRequirement [
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
			val osRequirement = osRequirements.get(0)
			if (osRequirement.linux)
				ct.setOSRequirement (SupportedOS.LINUX)
			else if (osRequirement.android)
				ct.setOSRequirement (SupportedOS.ANDROID)
		}
				
		// Store middleware requirement.
		// NOTE: Only first should/will be stored.
		if (middlewareRequirements.size() > 0) {
			val middlewareRequirement = middlewareRequirements.get(0)
			if (middlewareRequirement.rtidds)
				ct.setMiddlewareRequirement (SupportedMiddleware.RTIDDS)
			else if (middlewareRequirement.alljoyn)
				ct.setMiddlewareRequirement (SupportedMiddleware.ALLJOYN)
			else if (middlewareRequirement.lcm)
				ct.setMiddlewareRequirement (SupportedMiddleware.LCM)
		}
		
		// Store artifact requirements.
		// NOTE: Artifacts could be more than one.
		for (a : artifactRequirements)
			ct.addArtifactRequirement (a.getArtifact().getName())
			
		// Store device requirements.
		// NOTE: Devices could be more than one.
		for (d: deviceRequirements)
			ct.addDeviceRequirement (d.getDevice().getName())
	}
	
	/*
	 * 
	 */
	def generateNodeCategories (Iterable<NodesCategory> nodeCategories, 
								Iterable<NodeTemplate> nodeTemplates,
								DB db) {
		// Loop through each node category.
		for (nc : nodeCategories) {
			val DM_NodeCategory nodeCategory = new DM_NodeCategory()
			
			nodeCategory.init()
			
			// Store name.
			nodeCategory.setName (nc.getName())
			
			// Loop through each node template and add nodes templates that are part 
			// of above nodeCategory.
			for (nt : nodeTemplates) {
				var boolean generateNodeTemplate = false
				
				val nodeCategoryLabels = nt.getNodeTemplateInfo().filter(NodeCategoryLabel)
				for (ncl : nodeCategoryLabels) {
					for (l : ncl.getLabel()) {
						if (l.getName().equals (nc.getName())) {
							generateNodeTemplate = true	
						}
					}
				}
				
				// If node template is part of this category then generate and store
				// related information.
				if (generateNodeTemplate) {
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
							val os = nt.getNodeTemplateInfo().filter(OSSupported).get(0)
							if (os.linux)
								setOS (SupportedOS::LINUX)
							if (os.android)
								setOS (SupportedOS::ANDROID)
						}
						
						if (nt.getNodeTemplateInfo().filter(Middleware).size() > 0) {
							val middlewareList = nt.getNodeTemplateInfo().filter(Middleware).get(0)
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
								
								// Store device reliability and lifetime.
								setReliability (d.getReliability())
								
								// Store lifetime.
								setLifetime [
									val lifetime = d.getLifetime()
									val unit = d.getUnit()
									
									setLifetime (lifetime)
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
			}
			
			nodeCategory.insert (db)	
		}
	}
	
	/*
	 * 
	 */
	def generateSystems (Iterable<SystemDescription> systems, DB db) {
		// Loop through each system.
		for (s : systems) {
			val DM_SystemDescription system = new DM_SystemDescription()
			
			system.init()
			
			// Store name.
			system.setName (s.getName())
			
			// Store reliability threshold.
			system.setReliabilityThreshold (s.getReliabilityThreshold())
			
			// Store constraints.
			for (c : s.getConstraints()) {
				system.addConstraint [
					init()
					if(c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ConsensusReplicationConstraintImpl")) {
						setKind(SystemConstraintKind::CONSENSUS_REPLICATION)
						addFunctionality((c as ConsensusReplicationConstraint).getFunctionality().getName())
						setMinInstances((c as ConsensusReplicationConstraint).getRange().getLower())
						setMaxInstances((c as ConsensusReplicationConstraint).getRange().getUpper())
						setNumInstances((c as ConsensusReplicationConstraint).getRange().getExact())
						setServiceComponentType((c as ConsensusReplicationConstraint).getServiceComponent().getName())
					}
					
					if(c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.ActiveReplicationConstraintImpl")) {
						setKind(SystemConstraintKind::CLUSTER_REPLICATION)
						addFunctionality((c as ActiveReplicationConstraint).getFunctionality().getName())
						setMinInstances((c as ActiveReplicationConstraint).getRange().getLower())
						setMaxInstances((c as ActiveReplicationConstraint).getRange().getUpper())
						setNumInstances((c as ActiveReplicationConstraint).getRange().getExact())
					}
						
					if(c.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.VoterReplicationConstraintImpl")) {
						setKind(SystemConstraintKind::VOTER_REPLICATION)
						addFunctionality((c as VoterReplicationConstraint).getFunctionality().getName())
						setMinInstances((c as VoterReplicationConstraint).getRange().getLower())
						setMaxInstances((c as VoterReplicationConstraint).getRange().getUpper())
						setNumInstances((c as VoterReplicationConstraint).getRange().getExact())
						setServiceComponentType((c as VoterReplicationConstraint).getServiceComponent().getName())
					}
				]
			}
			
			// Store objectives.
			for (o : s.getRequiredobjectives()) {
				system.addObjective [
					init()
					setName(o.getName())
					setIsLocal(o.isLocal)
					
					// If local objective, store corresponding node categories.
					// "Per node" requirement will be associated later.
					if (o.isLocal) {
						for (oc : o.getConstraints()) {
							if(oc.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.CategoryConstraintImpl")) {
								for (category : (oc as CategoryConstraint).getCategories())
									addNodeCategory(category.getName())
							}
						}
					}
					
					// Store functionalities.
					val functionalityMap = getFunctionalities (o.getComposition())
					
					val addedFunctionalities = new ArrayList<String>()
					
					// First add keys of the functionalitiyMap. These keys represent functionalities that
					// have dependencies.
					for (f : functionalityMap.keys()) {
						if (!addedFunctionalities.contains(f)) {
							addFunctionality[
								init()
								setName(f)
								for (d : functionalityMap.get(f))
									addDependsOn(d)
								// Check and set "per node" requirement flag.
								for (oc : o.getConstraints()) {
									if(oc.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.perNodeFunctionalityImpl")) {
										for (functionality: (oc as perNodeFunctionality).getFunctionality()) {
											if (functionality.getName().equals(f))
												setPerNode(true)
										}
									}
								}
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
								
								// Check and set "per node" requirement flag.
								for (oc : o.getConstraints()) {
									if(oc.class.name.equals("edu.vanderbilt.isis.chariot.chariot.impl.perNodeFunctionalityImpl")) {
										for (functionality: (oc as perNodeFunctionality).getFunctionality()) {
											if (functionality.getName().equals(f))
												setPerNode(true)
										}
									}
								}
							]
							addedFunctionalities.add(f)
						}
					}
				]
			}
			
			// Generate nodes and deployment.
			generateNodes (s.getNodes(), db)
			
			system.insert(db)
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
	
	/*
	 * 
	 */
	def generateNodes (Iterable<Node> nodes, DB db) {
		// Loop through each node.
		for (n : nodes) {
			val DM_Node node = new DM_Node()
			
			node.init()
			
			// Store name.
			node.setName (n.getName())
			
			// Store reliability.
			node.setReliability (n.getReliability())
			
			// Store lifetime.
			node.setLifetime [
				val lifetime = n.getLifetime()
				val unit = n.getUnit()
				
				setLifetime (lifetime)
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
			
			// Filter and store node template label:
			// NOTE: Only first should/will be stored.
			val nodeTemplates = n.getNodeInfo().filter(NodeTemplateLabel)
			if (nodeTemplates.size() > 0)
				node.setNodeTemplate(nodeTemplates.get(0).getTemplate().getName())
				
			// Set status to be ACTIVE.
			node.setStatus(Status::ACTIVE)
			
			// Filter and store interfaces.
			// NOTE: Interfaces can be one or more.
			for (i : n.getNodeInfo().filter(NetworkInterface)) {
				node.addInterface [
					init()
					setName(i.getName())
					setAddress(i.getAddress())
					setNetwork(i.getNetwork())
				]
			}
			
			node.insert(db)
		}
	}
}