package edu.vanderbilt.isis.chariot.datamodel.SystemDescription;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_Functionality implements IMongoBean {
  /**
   * Creates a new DM_Functionality wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Functionality(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Functionality wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Functionality() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_Functionality");
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
  
  public List<String> getDependsOn() {
    return (List<String>) _dbObject.get("dependsOn");
  }
  
  public void setDependsOn(final List<String> dependsOn) {
    _dbObject.put("dependsOn", dependsOn);
  }
  
  public boolean getPerNode() {
    return (Boolean) _dbObject.get("perNode");
  }
  
  public void setPerNode(final boolean perNode) {
    _dbObject.put("perNode", perNode);
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setDependsOn(_arrayList);
    this.setPerNode(false);
  }
  
  public void addDependsOn(final String dependsOn) {
    final Logger LOGGER = Logger.getLogger("DM_SystemDescription");
    List<String> _dependsOn = this.getDependsOn();
    boolean _equals = Objects.equal(_dependsOn, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setDependsOn(_arrayList);
    }
    List<String> _dependsOn_1 = this.getDependsOn();
    boolean _contains = _dependsOn_1.contains(dependsOn);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _dependsOn_2 = this.getDependsOn();
      _dependsOn_2.add(dependsOn);
    } else {
      String _name = this.getName();
      String _plus = ((dependsOn + 
        " functionality already exists as dependency for functionality ") + _name);
      LOGGER.info(_plus);
    }
  }
}
