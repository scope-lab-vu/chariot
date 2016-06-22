package edu.vanderbilt.isis.chariot.datamodel.SystemDescription;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_Functionality;
import java.util.List;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;

@SuppressWarnings("all")
public class DM_Objective implements IMongoBean {
  /**
   * Creates a new DM_Objective wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Objective(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Objective wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Objective() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_Objective");
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
  
  private MongoBeanList<DM_Functionality> _functionalities;
  
  public List<DM_Functionality> getFunctionalities() {
    if(_functionalities==null)
    	_functionalities = new MongoBeanList<DM_Functionality>(_dbObject, "functionalities");
    return _functionalities;
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.getFunctionalities();
  }
  
  public void addFunctionality(final Procedure1<? super DM_Functionality> initializer) {
    DM_Functionality _dM_Functionality = new DM_Functionality();
    final DM_Functionality functionalityToAdd = ObjectExtensions.<DM_Functionality>operator_doubleArrow(_dM_Functionality, initializer);
    List<DM_Functionality> _functionalities = this.getFunctionalities();
    _functionalities.add(functionalityToAdd);
  }
}
