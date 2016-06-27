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
  
  public String getFunctionality() {
    return (String) _dbObject.get("functionality");
  }
  
  public void setFunctionality(final String functionality) {
    _dbObject.put("functionality", functionality);
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
  
  public List<String> getNodeCategories() {
    return (List<String>) _dbObject.get("nodeCategories");
  }
  
  public void setNodeCategories(final List<String> nodeCategories) {
    _dbObject.put("nodeCategories", nodeCategories);
  }
  
  public void init() {
    String _string = new String();
    this.setKind(_string);
    String _string_1 = new String();
    this.setFunctionality(_string_1);
    this.setMaxInstances(0);
    this.setMinInstances(0);
    this.setNumInstances(0);
    String _string_2 = new String();
    this.setServiceComponentType(_string_2);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setNodeCategories(_arrayList);
  }
  
  public void setKind(final SystemConstraintKind kind) {
    String _string = kind.toString();
    this.setKind(_string);
  }
  
  public void addNodeCategory(final String nodeCategory) {
    final Logger LOGGER = Logger.getLogger("DM_SystemConstraint");
    List<String> _nodeCategories = this.getNodeCategories();
    boolean _equals = Objects.equal(_nodeCategories, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setNodeCategories(_arrayList);
    }
    List<String> _nodeCategories_1 = this.getNodeCategories();
    boolean _contains = _nodeCategories_1.contains(nodeCategory);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _nodeCategories_2 = this.getNodeCategories();
      _nodeCategories_2.add(nodeCategory);
    } else {
      LOGGER.info((nodeCategory + 
        " node category already exists"));
    }
  }
}
