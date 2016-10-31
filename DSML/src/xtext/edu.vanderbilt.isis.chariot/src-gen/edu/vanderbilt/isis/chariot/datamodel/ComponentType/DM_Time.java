package edu.vanderbilt.isis.chariot.datamodel.ComponentType;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.TimeUnit;
import org.xtext.mongobeans.lib.IMongoBean;

/**
 * An entity to store time and unit.
 */
@SuppressWarnings("all")
public class DM_Time implements IMongoBean {
  /**
   * Creates a new DM_Time wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Time(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Time wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Time() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_Time");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public double getTime() {
    return (Double) _dbObject.get("time");
  }
  
  public void setTime(final double time) {
    _dbObject.put("time", time);
  }
  
  public String getUnit() {
    return (String) _dbObject.get("unit");
  }
  
  public void setUnit(final String unit) {
    _dbObject.put("unit", unit);
  }
  
  /**
   * Method to set unit of time.
   * 
   * @param unit	Unit of time.
   */
  public void setUnit(final TimeUnit unit) {
    String _string = unit.toString();
    this.setUnit(_string);
  }
}
