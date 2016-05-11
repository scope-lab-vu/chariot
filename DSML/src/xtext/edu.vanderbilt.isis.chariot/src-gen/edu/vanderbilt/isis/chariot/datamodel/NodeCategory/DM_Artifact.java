package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_Artifact implements IMongoBean {
  /**
   * Creates a new DM_Artifact wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Artifact(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Artifact wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Artifact() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Artifact");
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
  
  public String getLocation() {
    return (String) _dbObject.get("location");
  }
  
  public void setLocation(final String location) {
    _dbObject.put("location", location);
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    String _string_1 = new String();
    this.setLocation(_string_1);
  }
}
