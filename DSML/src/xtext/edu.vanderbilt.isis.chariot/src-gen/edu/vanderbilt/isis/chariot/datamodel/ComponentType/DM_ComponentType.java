package edu.vanderbilt.isis.chariot.datamodel.ComponentType;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_Time;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Memory;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Storage;
import edu.vanderbilt.isis.chariot.datamodel.SupportedMiddleware;
import edu.vanderbilt.isis.chariot.datamodel.SupportedOS;
import edu.vanderbilt.isis.chariot.generator.ConfigSpaceGenerator;
import java.util.ArrayList;
import java.util.List;
import org.bson.types.ObjectId;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
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
  
  public String getProvidedFunctionality() {
    return (String) _dbObject.get("providedFunctionality");
  }
  
  public void setProvidedFunctionality(final String providedFunctionality) {
    _dbObject.put("providedFunctionality", providedFunctionality);
  }
  
  public DM_Memory getRequiredMemory() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("requiredMemory"));
  }
  
  public void setRequiredMemory(final DM_Memory requiredMemory) {
    _dbObject.put("requiredMemory", WrappingUtil.unwrap(requiredMemory));
  }
  
  public DM_Storage getRequiredStorage() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("requiredStorage"));
  }
  
  public void setRequiredStorage(final DM_Storage requiredStorage) {
    _dbObject.put("requiredStorage", WrappingUtil.unwrap(requiredStorage));
  }
  
  public String getRequiredOS() {
    return (String) _dbObject.get("requiredOS");
  }
  
  public void setRequiredOS(final String requiredOS) {
    _dbObject.put("requiredOS", requiredOS);
  }
  
  public String getRequiredMiddleware() {
    return (String) _dbObject.get("requiredMiddleware");
  }
  
  public void setRequiredMiddleware(final String requiredMiddleware) {
    _dbObject.put("requiredMiddleware", requiredMiddleware);
  }
  
  public List<String> getRequiredArtifacts() {
    return (List<String>) _dbObject.get("requiredArtifacts");
  }
  
  public void setRequiredArtifacts(final List<String> requiredArtifacts) {
    _dbObject.put("requiredArtifacts", requiredArtifacts);
  }
  
  public List<String> getRequiredDevices() {
    return (List<String>) _dbObject.get("requiredDevices");
  }
  
  public void setRequiredDevices(final List<String> requiredDevices) {
    _dbObject.put("requiredDevices", requiredDevices);
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
  
  public DM_Time getPeriod() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("period"));
  }
  
  public void setPeriod(final DM_Time period) {
    _dbObject.put("period", WrappingUtil.unwrap(period));
  }
  
  public DM_Time getDeadline() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("deadline"));
  }
  
  public void setDeadline(final DM_Time deadline) {
    _dbObject.put("deadline", WrappingUtil.unwrap(deadline));
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    String _string_1 = new String();
    this.setProvidedFunctionality(_string_1);
    DM_Memory _dM_Memory = new DM_Memory();
    final Procedure1<DM_Memory> _function = (DM_Memory it) -> {
      it.setMemory(0);
      it.setUnit("");
    };
    DM_Memory _doubleArrow = ObjectExtensions.<DM_Memory>operator_doubleArrow(_dM_Memory, _function);
    this.setRequiredMemory(_doubleArrow);
    DM_Storage _dM_Storage = new DM_Storage();
    final Procedure1<DM_Storage> _function_1 = (DM_Storage it) -> {
      it.setStorage(0);
      it.setUnit("");
    };
    DM_Storage _doubleArrow_1 = ObjectExtensions.<DM_Storage>operator_doubleArrow(_dM_Storage, _function_1);
    this.setRequiredStorage(_doubleArrow_1);
    String _string_2 = new String();
    this.setRequiredOS(_string_2);
    String _string_3 = new String();
    this.setRequiredMiddleware(_string_3);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setRequiredArtifacts(_arrayList);
    ArrayList<String> _arrayList_1 = new ArrayList<String>();
    this.setRequiredDevices(_arrayList_1);
    String _string_4 = new String();
    this.setStartScript(_string_4);
    String _string_5 = new String();
    this.setStopScript(_string_5);
    DM_Time _dM_Time = new DM_Time();
    final Procedure1<DM_Time> _function_2 = (DM_Time it) -> {
      it.setTime(0.0);
      it.setUnit("");
    };
    DM_Time _doubleArrow_2 = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time, _function_2);
    this.setPeriod(_doubleArrow_2);
    DM_Time _dM_Time_1 = new DM_Time();
    final Procedure1<DM_Time> _function_3 = (DM_Time it) -> {
      it.setTime(0.0);
      it.setUnit("");
    };
    DM_Time _doubleArrow_3 = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time_1, _function_3);
    this.setDeadline(_doubleArrow_3);
  }
  
  public void setRequiredMemory(final Procedure1<? super DM_Memory> initializer) {
    DM_Memory _dM_Memory = new DM_Memory();
    DM_Memory _doubleArrow = ObjectExtensions.<DM_Memory>operator_doubleArrow(_dM_Memory, initializer);
    this.setRequiredMemory(_doubleArrow);
  }
  
  public void setRequiredStorage(final Procedure1<? super DM_Storage> initializer) {
    DM_Storage _dM_Storage = new DM_Storage();
    DM_Storage _doubleArrow = ObjectExtensions.<DM_Storage>operator_doubleArrow(_dM_Storage, initializer);
    this.setRequiredStorage(_doubleArrow);
  }
  
  public void setRequiredOS(final SupportedOS os) {
    String _string = os.toString();
    this.setRequiredOS(_string);
  }
  
  public void setRequiredMiddleware(final SupportedMiddleware middleware) {
    String _string = middleware.toString();
    this.setRequiredMiddleware(_string);
  }
  
  public void addRequiredArtifact(final String artifact) {
    List<String> _requiredArtifacts = this.getRequiredArtifacts();
    boolean _equals = Objects.equal(_requiredArtifacts, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setRequiredArtifacts(_arrayList);
    }
    List<String> _requiredArtifacts_1 = this.getRequiredArtifacts();
    boolean _contains = _requiredArtifacts_1.contains(artifact);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _requiredArtifacts_2 = this.getRequiredArtifacts();
      _requiredArtifacts_2.add(artifact);
    } else {
      String _name = this.getName();
      String _plus = ((artifact + 
        " artifact already exists in component ") + _name);
      ConfigSpaceGenerator.LOGGER.info(_plus);
    }
  }
  
  public void addRequiredDevice(final String device) {
    List<String> _requiredDevices = this.getRequiredDevices();
    boolean _equals = Objects.equal(_requiredDevices, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setRequiredDevices(_arrayList);
    }
    List<String> _requiredDevices_1 = this.getRequiredDevices();
    boolean _contains = _requiredDevices_1.contains(device);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _requiredDevices_2 = this.getRequiredDevices();
      _requiredDevices_2.add(device);
    } else {
      String _name = this.getName();
      String _plus = ((device + 
        " device already exists in component ") + _name);
      ConfigSpaceGenerator.LOGGER.info(_plus);
    }
  }
  
  public void setPeriod(final Procedure1<? super DM_Time> initializer) {
    DM_Time _dM_Time = new DM_Time();
    DM_Time _doubleArrow = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time, initializer);
    this.setPeriod(_doubleArrow);
  }
  
  public void setDeadline(final Procedure1<? super DM_Time> initializer) {
    DM_Time _dM_Time = new DM_Time();
    DM_Time _doubleArrow = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time, initializer);
    this.setDeadline(_doubleArrow);
  }
  
  public void insert(final DB database) {
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
      ConfigSpaceGenerator.LOGGER.info(_plus);
    } else {
      String _name_1 = this.getName();
      String _plus_1 = (_name_1 + 
        " component type already exists. Trying to update");
      ConfigSpaceGenerator.LOGGER.info(_plus_1);
      this.update(result, dbCollection);
    }
  }
  
  public void update(final DBObject objectToUpdate, final DBCollection targetCollection) {
    targetCollection.remove(objectToUpdate);
    DBObject _dbObject = this.getDbObject();
    targetCollection.save(_dbObject);
    String _name = this.getName();
    String _plus = (_name + 
      " component type has been updated.");
    ConfigSpaceGenerator.LOGGER.info(_plus);
  }
}
