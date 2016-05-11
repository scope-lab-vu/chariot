package edu.vanderbilt.isis.chariot.datamodel.Node;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.Status;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_Component implements IMongoBean {
  /**
   * Creates a new DM_Component wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Component(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Component wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Component() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.Node.DM_Component");
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
  
  public String getStatus() {
    return (String) _dbObject.get("status");
  }
  
  public void setStatus(final String status) {
    _dbObject.put("status", status);
  }
  
  public String getType() {
    return (String) _dbObject.get("type");
  }
  
  public void setType(final String type) {
    _dbObject.put("type", type);
  }
  
  public String getMode() {
    return (String) _dbObject.get("mode");
  }
  
  public void setMode(final String mode) {
    _dbObject.put("mode", mode);
  }
  
  public String getFunctionalityInstance() {
    return (String) _dbObject.get("functionalityInstance");
  }
  
  public void setFunctionalityInstance(final String functionalityInstance) {
    _dbObject.put("functionalityInstance", functionalityInstance);
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    String _string_1 = new String();
    this.setStatus(_string_1);
    String _string_2 = new String();
    this.setType(_string_2);
    String _string_3 = new String();
    this.setMode(_string_3);
    String _string_4 = new String();
    this.setFunctionalityInstance(_string_4);
  }
  
  public void setStatus(final Status status) {
    String _string = status.toString();
    this.setStatus(_string);
  }
}
