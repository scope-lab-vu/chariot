package edu.vanderbilt.isis.chariot.datamodel.GoalDescription;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.generator.ConfigSpaceGenerator;
import java.util.ArrayList;
import java.util.List;
import org.xtext.mongobeans.lib.IMongoBean;

/**
 * An entity to store functionality.
 */
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
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.GoalDescription.DM_Functionality");
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
  
  /**
   * Initialization method.
   */
  public void init() {
    String _string = new String();
    this.setName(_string);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setDependsOn(_arrayList);
  }
  
  /**
   * Method to add functionality dependency.
   * 
   * @param dependsOn	Name of the functionality on which this
   * 					functionality depends on.
   */
  public void addDependsOn(final String dependsOn) {
    List<String> _dependsOn = this.getDependsOn();
    boolean _contains = _dependsOn.contains(dependsOn);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _dependsOn_1 = this.getDependsOn();
      _dependsOn_1.add(dependsOn);
    } else {
      String _name = this.getName();
      String _plus = ((dependsOn + 
        " functionality already exists as dependency for functionality ") + _name);
      ConfigSpaceGenerator.LOGGER.info(_plus);
    }
  }
}
