package edu.vanderbilt.isis.chariot.datamodel.ComponentType;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.TimeUnit;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_Period implements IMongoBean {
  /**
   * Creates a new DM_Period wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Period(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Period wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Period() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_Period");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public double getPeriod() {
    return (Double) _dbObject.get("period");
  }
  
  public void setPeriod(final double period) {
    _dbObject.put("period", period);
  }
  
  public String getUnit() {
    return (String) _dbObject.get("unit");
  }
  
  public void setUnit(final String unit) {
    _dbObject.put("unit", unit);
  }
  
  public void setUnit(final TimeUnit unit) {
    String _string = unit.toString();
    this.setUnit(_string);
  }
}
