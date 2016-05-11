package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Artifact;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_AvailableMemory;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_AvailableStorage;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Device;
import edu.vanderbilt.isis.chariot.datamodel.SupportedMiddleware;
import edu.vanderbilt.isis.chariot.datamodel.SupportedOS;
import java.util.List;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;
import org.xtext.mongobeans.lib.WrappingUtil;

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
  
  public DM_AvailableMemory getAvailableMemory() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("availableMemory"));
  }
  
  public void setAvailableMemory(final DM_AvailableMemory availableMemory) {
    _dbObject.put("availableMemory", WrappingUtil.unwrap(availableMemory));
  }
  
  public DM_AvailableStorage getAvailableStorage() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("availableStorage"));
  }
  
  public void setAvailableStorage(final DM_AvailableStorage availableStorage) {
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
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    DM_AvailableMemory _dM_AvailableMemory = new DM_AvailableMemory();
    final Procedure1<DM_AvailableMemory> _function = (DM_AvailableMemory it) -> {
      it.setMemory(0);
      it.setUnit("");
    };
    DM_AvailableMemory _doubleArrow = ObjectExtensions.<DM_AvailableMemory>operator_doubleArrow(_dM_AvailableMemory, _function);
    this.setAvailableMemory(_doubleArrow);
    DM_AvailableStorage _dM_AvailableStorage = new DM_AvailableStorage();
    final Procedure1<DM_AvailableStorage> _function_1 = (DM_AvailableStorage it) -> {
      it.setStorage(0);
      it.setUnit("");
    };
    DM_AvailableStorage _doubleArrow_1 = ObjectExtensions.<DM_AvailableStorage>operator_doubleArrow(_dM_AvailableStorage, _function_1);
    this.setAvailableStorage(_doubleArrow_1);
    String _string_1 = new String();
    this.setOS(_string_1);
    String _string_2 = new String();
    this.setMiddleware(_string_2);
    this.getArtifacts();
    this.getDevices();
  }
  
  public void setAvailableMemory(final Procedure1<? super DM_AvailableMemory> initializer) {
    DM_AvailableMemory _dM_AvailableMemory = new DM_AvailableMemory();
    DM_AvailableMemory _doubleArrow = ObjectExtensions.<DM_AvailableMemory>operator_doubleArrow(_dM_AvailableMemory, initializer);
    this.setAvailableMemory(_doubleArrow);
  }
  
  public void setAvailableStorage(final Procedure1<? super DM_AvailableStorage> initializer) {
    DM_AvailableStorage _dM_AvailableStorage = new DM_AvailableStorage();
    DM_AvailableStorage _doubleArrow = ObjectExtensions.<DM_AvailableStorage>operator_doubleArrow(_dM_AvailableStorage, initializer);
    this.setAvailableStorage(_doubleArrow);
  }
  
  public void setOS(final SupportedOS os) {
    String _string = os.toString();
    this.setOS(_string);
  }
  
  public void setMiddleware(final SupportedMiddleware middleware) {
    String _string = middleware.toString();
    this.setMiddleware(_string);
  }
  
  public void addArtifact(final Procedure1<? super DM_Artifact> initializer) {
    DM_Artifact _dM_Artifact = new DM_Artifact();
    final DM_Artifact artifactToAdd = ObjectExtensions.<DM_Artifact>operator_doubleArrow(_dM_Artifact, initializer);
    List<DM_Artifact> _artifacts = this.getArtifacts();
    _artifacts.add(artifactToAdd);
  }
  
  public void addDevice(final Procedure1<? super DM_Device> initializer) {
    DM_Device _dM_Device = new DM_Device();
    final DM_Device deviceToAdd = ObjectExtensions.<DM_Device>operator_doubleArrow(_dM_Device, initializer);
    List<DM_Device> _devices = this.getDevices();
    _devices.add(deviceToAdd);
  }
}
