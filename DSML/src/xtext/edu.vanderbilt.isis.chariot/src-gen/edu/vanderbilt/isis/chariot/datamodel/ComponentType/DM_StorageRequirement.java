package edu.vanderbilt.isis.chariot.datamodel.ComponentType;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.StorageUnit;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_StorageRequirement implements IMongoBean {
  /**
   * Creates a new DM_StorageRequirement wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_StorageRequirement(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_StorageRequirement wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_StorageRequirement() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_StorageRequirement");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public int getStorage() {
    return (Integer) _dbObject.get("storage");
  }
  
  public void setStorage(final int storage) {
    _dbObject.put("storage", storage);
  }
  
  public String getUnit() {
    return (String) _dbObject.get("unit");
  }
  
  public void setUnit(final String unit) {
    _dbObject.put("unit", unit);
  }
  
  public void setUnit(final StorageUnit unit) {
    String _string = unit.toString();
    this.setUnit(_string);
  }
}
