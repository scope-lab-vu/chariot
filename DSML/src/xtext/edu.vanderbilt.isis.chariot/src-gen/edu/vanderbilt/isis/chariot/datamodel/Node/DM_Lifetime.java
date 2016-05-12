package edu.vanderbilt.isis.chariot.datamodel.Node;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.TimeUnit;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_Lifetime implements IMongoBean {
  /**
   * Creates a new DM_Lifetime wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Lifetime(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Lifetime wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Lifetime() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.Node.DM_Lifetime");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public double getLifetime() {
    return (Double) _dbObject.get("lifetime");
  }
  
  public void setLifetime(final double lifetime) {
    _dbObject.put("lifetime", lifetime);
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
