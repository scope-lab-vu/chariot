package edu.vanderbilt.isis.chariot.datamodel.SystemDescription;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_Functionality;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
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
  
  public boolean getIsLocal() {
    return (Boolean) _dbObject.get("isLocal");
  }
  
  public void setIsLocal(final boolean isLocal) {
    _dbObject.put("isLocal", isLocal);
  }
  
  public List<String> getNodeCategories() {
    return (List<String>) _dbObject.get("nodeCategories");
  }
  
  public void setNodeCategories(final List<String> nodeCategories) {
    _dbObject.put("nodeCategories", nodeCategories);
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
    this.setIsLocal(false);
    ArrayList<String> _arrayList = new ArrayList<String>();
    this.setNodeCategories(_arrayList);
    this.getFunctionalities();
  }
  
  public void addNodeCategory(final String nodeCategory) {
    final Logger LOGGER = Logger.getLogger("DM_Objective");
    List<String> _nodeCategories = this.getNodeCategories();
    boolean _equals = Objects.equal(_nodeCategories, null);
    if (_equals) {
      ArrayList<String> _arrayList = new ArrayList<String>();
      this.setNodeCategories(_arrayList);
    }
    List<String> _nodeCategories_1 = this.getNodeCategories();
    boolean _contains = _nodeCategories_1.contains(nodeCategory);
    boolean _not = (!_contains);
    if (_not) {
      List<String> _nodeCategories_2 = this.getNodeCategories();
      _nodeCategories_2.add(nodeCategory);
    } else {
      String _name = this.getName();
      String _plus = ((nodeCategory + 
        " node category already exists in objective ") + _name);
      LOGGER.info(_plus);
    }
  }
  
  public void addFunctionality(final Procedure1<? super DM_Functionality> initializer) {
    DM_Functionality _dM_Functionality = new DM_Functionality();
    final DM_Functionality functionalityToAdd = ObjectExtensions.<DM_Functionality>operator_doubleArrow(_dM_Functionality, initializer);
    List<DM_Functionality> _functionalities = this.getFunctionalities();
    _functionalities.add(functionalityToAdd);
  }
}
