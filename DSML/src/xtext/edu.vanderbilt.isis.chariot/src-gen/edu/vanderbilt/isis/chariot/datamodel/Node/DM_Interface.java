package edu.vanderbilt.isis.chariot.datamodel.Node;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_Interface implements IMongoBean {
  /**
   * Creates a new DM_Interface wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Interface(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Interface wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Interface() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.Node.DM_Interface");
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
  
  public String getAddress() {
    return (String) _dbObject.get("address");
  }
  
  public void setAddress(final String address) {
    _dbObject.put("address", address);
  }
  
  public String getNetwork() {
    return (String) _dbObject.get("network");
  }
  
  public void setNetwork(final String network) {
    _dbObject.put("network", network);
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    String _string_1 = new String();
    this.setAddress(_string_1);
    String _string_2 = new String();
    this.setNetwork(_string_2);
  }
}
