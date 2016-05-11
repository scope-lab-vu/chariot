package edu.vanderbilt.isis.chariot.datamodel.ComponentType;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_MemoryRequirement;
import edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_Mode;
import edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_StorageRequirement;
import edu.vanderbilt.isis.chariot.datamodel.SupportedMiddleware;
import edu.vanderbilt.isis.chariot.datamodel.SupportedOS;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
import org.bson.types.ObjectId;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;
import org.xtext.mongobeans.lib.WrappingUtil;

@SuppressWarnings("all")
public class DM_ComponentType implements IMongoBean {
  /**
   * Creates a new DM_ComponentType wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_ComponentType(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_ComponentType wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_ComponentType() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_ComponentType");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public ObjectId get_id() {
    return (ObjectId) _dbObject.get("_id");
  }
  
  public void set_id(final ObjectId _id) {
    _dbObject.put("_id", _id);
  }
  
  public String getName() {
    return (String) _dbObject.get("name");
  }
  
  public void setName(final String name) {
    _dbObject.put("name", name);
  }
  
  public List<String> getProvidedFunctionalities() {
    return (List<String>) _dbObject.get("providedFunctionalities");
  }
  
  public void setProvidedFunctionalities(final List<String> providedFunctionalities) {
    _dbObject.put("providedFunctionalities", providedFunctionalities);
  }
  
  private MongoBeanList<DM_Mode> _modes;
  
  public List<DM_Mode> getModes() {
    if(_modes==null)
    	_modes = new MongoBeanList<DM_Mode>(_dbObject, "modes");
    return _modes;
  }
  
  public DM_MemoryRequirement getMemoryRequirement() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("memoryRequirement"));
  }
  
  public void setMemoryRequirement(final DM_MemoryRequirement memoryRequirement) {
    _dbObject.put("memoryRequirement", WrappingUtil.unwrap(memoryRequirement));
  }
  
  public DM_StorageRequirement getStorageRequirement() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("storageRequirement"));
  }
  
  public void setStorageRequirement(final DM_StorageRequirement storageRequirement) {
    _dbObject.put("storageRequirement", WrappingUtil.unwrap(storageRequirement));
  }
  
  public String getOsRequirement() {
    return (String) _dbObject.get("osRequirement");
  }
  
  public void setOsRequirement(final String osRequirement) {
    _dbObject.put("osRequirement", osRequirement);
  }
  
  public String getMiddlewareRequirement() {
    return (String) _dbObject.get("middlewareRequirement");
  }
  
  public void setMiddlewareRequirement(final String middlewareRequirement) {
    _dbObject.put("middlewareRequirement", middlewareRequirement);
  }
  
  public List<String> getArtifactRequirements() {
    return (List<String>) _dbObject.get("artifactRequirements");
  }
  
  public void setArtifactRequirements(final List<String> artifactRequirements) {
    _dbObject.put("artifactRequirements", artifactRequirements);
  }
  
  public List<String> getDeviceRequirements() {
    return (List<String>) _dbObject.get("deviceRequirements");
  }
  
  public void setDeviceRequirements(final List<String> deviceRequirements) {
    _dbObject.put("deviceRequirements", deviceRequirements);
  }
  
  public String getStartScript() {
    return (String) _dbObject.get("startScript");
  }
  
  public void setStartScript(final String startScript) {
    _dbObject.put("startScript", startScript);
  }
  
  public String getStopScript() {
    return (String) _dbObject.get("stopScript");
  }
  
  public void setStopScript(final String stopScript) {
    _dbObject.put("stopScript", stopScript);
  }
  
  public double getPeriod() {
    return (Double) _dbObject.get("period");
  }
  
  public void setPeriod(final double period) {
    _dbObject.put("period", period);
  }
  
  public double getDeadline() {
    return (Double) _dbObject.get("deadline");
  }
  
  public void setDeadline(final double deadline) {
    _dbObject.put("deadline", deadline);
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setProvidedFunctionalities(_arrayList);
    this.getModes();
    DM_MemoryRequirement _dM_MemoryRequirement = new DM_MemoryRequirement();
    final Procedure1<DM_MemoryRequirement> _function = (DM_MemoryRequirement it) -> {
      it.setMemory(0);
      it.setUnit("");
    };
    DM_MemoryRequirement _doubleArrow = ObjectExtensions.<DM_MemoryRequirement>operator_doubleArrow(_dM_MemoryRequirement, _function);
    this.setMemoryRequirement(_doubleArrow);
    DM_StorageRequirement _dM_StorageRequirement = new DM_StorageRequirement();
    final Procedure1<DM_StorageRequirement> _function_1 = (DM_StorageRequirement it) -> {
      it.setStorage(0);
      it.setUnit("");
    };
    DM_StorageRequirement _doubleArrow_1 = ObjectExtensions.<DM_StorageRequirement>operator_doubleArrow(_dM_StorageRequirement, _function_1);
    this.setStorageRequirement(_doubleArrow_1);
    String _string_1 = new String();
    this.setOsRequirement(_string_1);
    String _string_2 = new String();
    this.setMiddlewareRequirement(_string_2);
    ArrayList<String> _arrayList_1 = new ArrayList<String>();
    this.setArtifactRequirements(_arrayList_1);
    ArrayList<String> _arrayList_2 = new ArrayList<String>();
    this.setDeviceRequirements(_arrayList_2);
    String _string_3 = new String();
    this.setStartScript(_string_3);
    String _string_4 = new String();
    this.setStopScript(_string_4);
    this.setPeriod(0);
    this.setDeadline(0);
  }
  
  public void addProvidedFunctionality(final String functionality) {
    final Logger LOGGER = Logger.getLogger("DM_ComponentType");
    List<String> _providedFunctionalities = this.getProvidedFunctionalities();
    boolean _equals = Objects.equal(_providedFunctionalities, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setProvidedFunctionalities(_arrayList);
    }
    List<String> _providedFunctionalities_1 = this.getProvidedFunctionalities();
    boolean _contains = _providedFunctionalities_1.contains(functionality);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _providedFunctionalities_2 = this.getProvidedFunctionalities();
      _providedFunctionalities_2.add(functionality);
    } else {
      String _name = this.getName();
      String _plus = ((functionality + 
        " functionality already exists in component ") + _name);
      LOGGER.info(_plus);
    }
  }
  
  public void addMode(final Procedure1<? super DM_Mode> initializer) {
    DM_Mode _dM_Mode = new DM_Mode();
    final DM_Mode modeToAdd = ObjectExtensions.<DM_Mode>operator_doubleArrow(_dM_Mode, initializer);
    List<DM_Mode> _modes = this.getModes();
    _modes.add(modeToAdd);
  }
  
  public void setMemoryRequirement(final Procedure1<? super DM_MemoryRequirement> initializer) {
    DM_MemoryRequirement _dM_MemoryRequirement = new DM_MemoryRequirement();
    DM_MemoryRequirement _doubleArrow = ObjectExtensions.<DM_MemoryRequirement>operator_doubleArrow(_dM_MemoryRequirement, initializer);
    this.setMemoryRequirement(_doubleArrow);
  }
  
  public void setStorageRequirement(final Procedure1<? super DM_StorageRequirement> initializer) {
    DM_StorageRequirement _dM_StorageRequirement = new DM_StorageRequirement();
    DM_StorageRequirement _doubleArrow = ObjectExtensions.<DM_StorageRequirement>operator_doubleArrow(_dM_StorageRequirement, initializer);
    this.setStorageRequirement(_doubleArrow);
  }
  
  public void setOSRequirement(final SupportedOS os) {
    String _string = os.toString();
    this.setOsRequirement(_string);
  }
  
  public void setMiddlewareRequirement(final SupportedMiddleware middleware) {
    String _string = middleware.toString();
    this.setMiddlewareRequirement(_string);
  }
  
  public void addArtifactRequirement(final String artifact) {
    final Logger LOGGER = Logger.getLogger("DM_ComponentType");
    List<String> _artifactRequirements = this.getArtifactRequirements();
    boolean _equals = Objects.equal(_artifactRequirements, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setArtifactRequirements(_arrayList);
    }
    List<String> _artifactRequirements_1 = this.getArtifactRequirements();
    boolean _contains = _artifactRequirements_1.contains(artifact);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _artifactRequirements_2 = this.getArtifactRequirements();
      _artifactRequirements_2.add(artifact);
    } else {
      String _name = this.getName();
      String _plus = ((artifact + 
        " artifact already exists in component ") + _name);
      LOGGER.info(_plus);
    }
  }
  
  public void addDeviceRequirement(final String device) {
    final Logger LOGGER = Logger.getLogger("DM_ComponentType");
    List<String> _deviceRequirements = this.getDeviceRequirements();
    boolean _equals = Objects.equal(_deviceRequirements, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setDeviceRequirements(_arrayList);
    }
    List<String> _deviceRequirements_1 = this.getDeviceRequirements();
    boolean _contains = _deviceRequirements_1.contains(device);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _deviceRequirements_2 = this.getDeviceRequirements();
      _deviceRequirements_2.add(device);
    } else {
      String _name = this.getName();
      String _plus = ((device + 
        " device already exists in component ") + _name);
      LOGGER.info(_plus);
    }
  }
  
  public void insert(final DB database) {
    final Logger LOGGER = Logger.getLogger("DM_ComponentType");
    final DBCollection dbCollection = database.getCollection("ComponentTypes");
    DM_ComponentType _dM_ComponentType = new DM_ComponentType();
    final Procedure1<DM_ComponentType> _function = (DM_ComponentType it) -> {
      String _name = this.getName();
      it.setName(_name);
    };
    DM_ComponentType _doubleArrow = ObjectExtensions.<DM_ComponentType>operator_doubleArrow(_dM_ComponentType, _function);
    DBObject _dbObject = _doubleArrow.getDbObject();
    final DBObject result = dbCollection.findOne(_dbObject);
    boolean _equals = Objects.equal(result, null);
    if (_equals) {
      DBObject _dbObject_1 = this.getDbObject();
      dbCollection.save(_dbObject_1);
      String _name = this.getName();
      String _plus = (_name + 
        " component type added to database");
      LOGGER.info(_plus);
    } else {
      String _name_1 = this.getName();
      String _plus_1 = (_name_1 + 
        " component type already exists. Trying to update");
      LOGGER.info(_plus_1);
      this.update(result, dbCollection);
    }
  }
  
  public void update(final DBObject objectToUpdate, final DBCollection targetCollection) {
    final Logger LOGGER = Logger.getLogger("DM_ComponentType");
    targetCollection.remove(objectToUpdate);
    DBObject _dbObject = this.getDbObject();
    targetCollection.save(_dbObject);
    String _name = this.getName();
    String _plus = (_name + 
      " component type has been updated.");
    LOGGER.info(_plus);
  }
}
