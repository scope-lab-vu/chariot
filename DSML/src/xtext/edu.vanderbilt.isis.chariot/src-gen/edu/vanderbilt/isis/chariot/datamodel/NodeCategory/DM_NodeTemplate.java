package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Artifact;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Device;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Memory;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Storage;
import edu.vanderbilt.isis.chariot.datamodel.SupportedMiddleware;
import edu.vanderbilt.isis.chariot.datamodel.SupportedOS;
import edu.vanderbilt.isis.chariot.generator.ConfigSpaceGenerator;
import java.util.List;
import org.eclipse.xtext.xbase.lib.Functions.Function1;
import org.eclipse.xtext.xbase.lib.ListExtensions;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;
import org.xtext.mongobeans.lib.WrappingUtil;

/**
 * An entity to store node template.
 */
@SuppressWarnings("all")
public class DM_NodeTemplate implements IMongoBean {
  /**
   * Creates a new DM_NodeTemplate wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_NodeTemplate(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_NodeTemplate wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_NodeTemplate() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_NodeTemplate");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public String getName() {
    return (String) _dbObject.get("name");
  }
  
  public void setName(final String name) {
    _dbObject.put("name", name);
  }
  
  public DM_Memory getAvailableMemory() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("availableMemory"));
  }
  
  public void setAvailableMemory(final DM_Memory availableMemory) {
    _dbObject.put("availableMemory", WrappingUtil.unwrap(availableMemory));
  }
  
  public DM_Storage getAvailableStorage() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("availableStorage"));
  }
  
  public void setAvailableStorage(final DM_Storage availableStorage) {
    _dbObject.put("availableStorage", WrappingUtil.unwrap(availableStorage));
  }
  
  public String getOS() {
    return (String) _dbObject.get("OS");
  }
  
  public void setOS(final String OS) {
    _dbObject.put("OS", OS);
  }
  
  public String getMiddleware() {
    return (String) _dbObject.get("middleware");
  }
  
  public void setMiddleware(final String middleware) {
    _dbObject.put("middleware", middleware);
  }
  
  private MongoBeanList<DM_Artifact> _artifacts;
  
  public List<DM_Artifact> getArtifacts() {
    if(_artifacts==null)
    	_artifacts = new MongoBeanList<DM_Artifact>(_dbObject, "artifacts");
    return _artifacts;
  }
  
  private MongoBeanList<DM_Device> _devices;
  
  public List<DM_Device> getDevices() {
    if(_devices==null)
    	_devices = new MongoBeanList<DM_Device>(_dbObject, "devices");
    return _devices;
  }
  
  /**
   * Initialization method.
   */
  public void init() {
    String _string = new String();
    this.setName(_string);
    DM_Memory _dM_Memory = new DM_Memory();
    final Procedure1<DM_Memory> _function = (DM_Memory it) -> {
      it.setMemory(0);
      it.setUnit("");
    };
    DM_Memory _doubleArrow = ObjectExtensions.<DM_Memory>operator_doubleArrow(_dM_Memory, _function);
    this.setAvailableMemory(_doubleArrow);
    DM_Storage _dM_Storage = new DM_Storage();
    final Procedure1<DM_Storage> _function_1 = (DM_Storage it) -> {
      it.setStorage(0);
      it.setUnit("");
    };
    DM_Storage _doubleArrow_1 = ObjectExtensions.<DM_Storage>operator_doubleArrow(_dM_Storage, _function_1);
    this.setAvailableStorage(_doubleArrow_1);
    String _string_1 = new String();
    this.setOS(_string_1);
    String _string_2 = new String();
    this.setMiddleware(_string_2);
    this.getArtifacts();
    this.getDevices();
  }
  
  /**
   * Method to set memory availability.
   * 
   * @param initializer	The DM_Memory entity that should be used to
   * 						set available memory.
   */
  public void setAvailableMemory(final Procedure1<? super DM_Memory> initializer) {
    DM_Memory _dM_Memory = new DM_Memory();
    DM_Memory _doubleArrow = ObjectExtensions.<DM_Memory>operator_doubleArrow(_dM_Memory, initializer);
    this.setAvailableMemory(_doubleArrow);
  }
  
  /**
   * Method to set storage availability.
   * 
   * @param initializer	The DM_Storage entity that should be used to
   * 						set available storage.
   */
  public void setAvailableStorage(final Procedure1<? super DM_Storage> initializer) {
    DM_Storage _dM_Storage = new DM_Storage();
    DM_Storage _doubleArrow = ObjectExtensions.<DM_Storage>operator_doubleArrow(_dM_Storage, initializer);
    this.setAvailableStorage(_doubleArrow);
  }
  
  /**
   * Method to set available OS.
   * 
   * @param os	The available OS.
   */
  public void setOS(final SupportedOS os) {
    String _string = os.toString();
    this.setOS(_string);
  }
  
  /**
   * Method to set available middleware.
   * 
   * @param middleware The available middleware.
   */
  public void setMiddleware(final SupportedMiddleware middleware) {
    String _string = middleware.toString();
    this.setMiddleware(_string);
  }
  
  /**
   * Method to add an available artifact.
   * 
   * @param initializer	DM_Artifact entity to be added.
   */
  public void addArtifact(final Procedure1<? super DM_Artifact> initializer) {
    DM_Artifact _dM_Artifact = new DM_Artifact();
    final DM_Artifact artifactToAdd = ObjectExtensions.<DM_Artifact>operator_doubleArrow(_dM_Artifact, initializer);
    List<DM_Artifact> _artifacts = this.getArtifacts();
    final Function1<DM_Artifact, String> _function = (DM_Artifact it) -> {
      return it.getName();
    };
    final List<String> curArtifacts = ListExtensions.<DM_Artifact, String>map(_artifacts, _function);
    String _name = artifactToAdd.getName();
    boolean _contains = curArtifacts.contains(_name);
    boolean _not = (!_contains);
    if (_not) {
      List<DM_Artifact> _artifacts_1 = this.getArtifacts();
      _artifacts_1.add(artifactToAdd);
    } else {
      String _name_1 = artifactToAdd.getName();
      String _plus = (_name_1 + 
        " artifact already exists in node template ");
      String _name_2 = this.getName();
      String _plus_1 = (_plus + _name_2);
      ConfigSpaceGenerator.LOGGER.info(_plus_1);
    }
  }
  
  /**
   * Method to add a device.
   * 
   * @param initializer	DM_Device entity to be added.
   */
  public void addDevice(final Procedure1<? super DM_Device> initializer) {
    DM_Device _dM_Device = new DM_Device();
    final DM_Device deviceToAdd = ObjectExtensions.<DM_Device>operator_doubleArrow(_dM_Device, initializer);
    List<DM_Device> _devices = this.getDevices();
    final Function1<DM_Device, String> _function = (DM_Device it) -> {
      return it.getName();
    };
    final List<String> curDevices = ListExtensions.<DM_Device, String>map(_devices, _function);
    String _name = deviceToAdd.getName();
    boolean _contains = curDevices.contains(_name);
    boolean _not = (!_contains);
    if (_not) {
      List<DM_Device> _devices_1 = this.getDevices();
      _devices_1.add(deviceToAdd);
    } else {
      String _name_1 = deviceToAdd.getName();
      String _plus = (_name_1 + 
        " device already exists in node template ");
      String _name_2 = this.getName();
      String _plus_1 = (_plus + _name_2);
      ConfigSpaceGenerator.LOGGER.info(_plus_1);
    }
  }
}
