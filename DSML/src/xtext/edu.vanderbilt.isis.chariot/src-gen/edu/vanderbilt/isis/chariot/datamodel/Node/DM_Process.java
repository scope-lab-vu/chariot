package edu.vanderbilt.isis.chariot.datamodel.Node;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.Node.DM_Component;
import edu.vanderbilt.isis.chariot.datamodel.Status;
import java.util.List;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;

@SuppressWarnings("all")
public class DM_Process implements IMongoBean {
  /**
   * Creates a new DM_Process wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Process(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Process wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Process() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.Node.DM_Process");
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
  
  public int getPid() {
    return (Integer) _dbObject.get("pid");
  }
  
  public void setPid(final int pid) {
    _dbObject.put("pid", pid);
  }
  
  public String getStatus() {
    return (String) _dbObject.get("status");
  }
  
  public void setStatus(final String status) {
    _dbObject.put("status", status);
  }
  
  private MongoBeanList<DM_Component> _components;
  
  public List<DM_Component> getComponents() {
    if(_components==null)
    	_components = new MongoBeanList<DM_Component>(_dbObject, "components");
    return _components;
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.setPid(0);
    String _string_1 = new String();
    this.setStatus(_string_1);
    this.getComponents();
  }
  
  public void setStatus(final Status status) {
    String _string = status.toString();
    this.setStatus(_string);
  }
  
  public void addComponent(final Procedure1<? super DM_Component> initializer) {
    DM_Component _dM_Component = new DM_Component();
    final DM_Component componentToAdd = ObjectExtensions.<DM_Component>operator_doubleArrow(_dM_Component, initializer);
    List<DM_Component> _components = this.getComponents();
    _components.add(componentToAdd);
  }
}
