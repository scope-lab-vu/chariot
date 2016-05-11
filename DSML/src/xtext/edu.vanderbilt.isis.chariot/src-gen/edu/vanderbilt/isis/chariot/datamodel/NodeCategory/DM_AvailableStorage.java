package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.StorageUnit;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_AvailableStorage implements IMongoBean {
  /**
   * Creates a new DM_AvailableStorage wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_AvailableStorage(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_AvailableStorage wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_AvailableStorage() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_AvailableStorage");
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
