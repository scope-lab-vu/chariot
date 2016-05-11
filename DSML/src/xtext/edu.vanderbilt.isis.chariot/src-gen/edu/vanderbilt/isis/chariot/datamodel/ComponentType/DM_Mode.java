package edu.vanderbilt.isis.chariot.datamodel.ComponentType;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
import org.xtext.mongobeans.lib.IMongoBean;

@SuppressWarnings("all")
public class DM_Mode implements IMongoBean {
  /**
   * Creates a new DM_Mode wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Mode(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Mode wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Mode() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.ComponentType.DM_Mode");
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
  
  public boolean getIsDefault() {
    return (Boolean) _dbObject.get("isDefault");
  }
  
  public void setIsDefault(final boolean isDefault) {
    _dbObject.put("isDefault", isDefault);
  }
  
  public List<String> getProvidedFunctionalities() {
    return (List<String>) _dbObject.get("providedFunctionalities");
  }
  
  public void setProvidedFunctionalities(final List<String> providedFunctionalities) {
    _dbObject.put("providedFunctionalities", providedFunctionalities);
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.setIsDefault(false);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setProvidedFunctionalities(_arrayList);
  }
  
  public void addProvidedFunctionality(final String functionality) {
    final Logger LOGGER = Logger.getLogger("DM_Mode");
    List<String> _providedFunctionalities = this.getProvidedFunctionalities();
    boolean _equals = Objects.equal(_providedFunctionalities, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setProvidedFunctionalities(_arrayList);
    }
    List<String> _providedFunctionalities_1 = this.getProvidedFunctionalities();
    boolean _contains = _providedFunctionalities_1.contains(functionality);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _providedFunctionalities_2 = this.getProvidedFunctionalities();
      _providedFunctionalities_2.add(functionality);
    } else {
      String _name = this.getName();
      String _plus = ((functionality + 
        " functionality already exists in mode ") + _name);
      LOGGER.info(_plus);
    }
  }
}
