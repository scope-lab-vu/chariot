package edu.vanderbilt.isis.chariot.datamodel.SystemDescription;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.SystemConstraintKind;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_SystemConstraint implements IMongoBean {
  /**
   * Creates a new DM_SystemConstraint wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_SystemConstraint(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_SystemConstraint wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_SystemConstraint() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_SystemConstraint");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public String getKind() {
    return (String) _dbObject.get("kind");
  }
  
  public void setKind(final String kind) {
    _dbObject.put("kind", kind);
  }
  
  public List<String> getFunctionalities() {
    return (List<String>) _dbObject.get("functionalities");
  }
  
  public void setFunctionalities(final List<String> functionalities) {
    _dbObject.put("functionalities", functionalities);
  }
  
  public int getMaxInstances() {
    return (Integer) _dbObject.get("maxInstances");
  }
  
  public void setMaxInstances(final int maxInstances) {
    _dbObject.put("maxInstances", maxInstances);
  }
  
  public int getMinInstances() {
    return (Integer) _dbObject.get("minInstances");
  }
  
  public void setMinInstances(final int minInstances) {
    _dbObject.put("minInstances", minInstances);
  }
  
  public int getNumInstances() {
    return (Integer) _dbObject.get("numInstances");
  }
  
  public void setNumInstances(final int numInstances) {
    _dbObject.put("numInstances", numInstances);
  }
  
  public String getServiceComponentType() {
    return (String) _dbObject.get("serviceComponentType");
  }
  
  public void setServiceComponentType(final String serviceComponentType) {
    _dbObject.put("serviceComponentType", serviceComponentType);
  }
  
  public void init() {
    String _string = new String();
    this.setKind(_string);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setFunctionalities(_arrayList);
    this.setMaxInstances(0);
    this.setMinInstances(0);
    this.setNumInstances(0);
    String _string_1 = new String();
    this.setServiceComponentType(_string_1);
  }
  
  public void setKind(final SystemConstraintKind kind) {
    String _string = kind.toString();
    this.setKind(_string);
  }
  
  public void addFunctionality(final String functionality) {
    final Logger LOGGER = Logger.getLogger("DM_SystemDescription");
    List<String> _functionalities = this.getFunctionalities();
    boolean _equals = Objects.equal(_functionalities, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setFunctionalities(_arrayList);
    }
    List<String> _functionalities_1 = this.getFunctionalities();
    boolean _contains = _functionalities_1.contains(functionality);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _functionalities_2 = this.getFunctionalities();
      _functionalities_2.add(functionality);
    } else {
      String _kind = this.getKind();
      String _plus = ((functionality + 
        " functionality already exists in system constraint of kind ") + _kind);
      LOGGER.info(_plus);
    }
  }
}
