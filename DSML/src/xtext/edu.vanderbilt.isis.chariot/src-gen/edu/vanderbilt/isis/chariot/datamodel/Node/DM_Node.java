package edu.vanderbilt.isis.chariot.datamodel.Node;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.Node.DM_Interface;
import edu.vanderbilt.isis.chariot.datamodel.Node.DM_Lifetime;
import edu.vanderbilt.isis.chariot.datamodel.Node.DM_Process;
import edu.vanderbilt.isis.chariot.datamodel.Status;
import java.util.List;
import java.util.logging.Logger;
import org.bson.types.ObjectId;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;
import org.xtext.mongobeans.lib.WrappingUtil;

@SuppressWarnings("all")
public class DM_Node implements IMongoBean {
  /**
   * Creates a new DM_Node wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Node(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Node wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Node() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.Node.DM_Node");
  }
  
  private DBObject _dbObject;
  
  public DBObject getDbObject() {
    return this._dbObject;
  }
  
  public ObjectId get_id() {
    return (ObjectId) _dbObject.get("_id");
  }
  
  public void set_id(final ObjectId _id) {
    _dbObject.put("_id", _id);
  }
  
  public String getName() {
    return (String) _dbObject.get("name");
  }
  
  public void setName(final String name) {
    _dbObject.put("name", name);
  }
  
  public double getReliability() {
    return (Double) _dbObject.get("reliability");
  }
  
  public void setReliability(final double reliability) {
    _dbObject.put("reliability", reliability);
  }
  
  public DM_Lifetime getLifetime() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("lifetime"));
  }
  
  public void setLifetime(final DM_Lifetime lifetime) {
    _dbObject.put("lifetime", WrappingUtil.unwrap(lifetime));
  }
  
  public String getNodeTemplate() {
    return (String) _dbObject.get("nodeTemplate");
  }
  
  public void setNodeTemplate(final String nodeTemplate) {
    _dbObject.put("nodeTemplate", nodeTemplate);
  }
  
  public String getStatus() {
    return (String) _dbObject.get("status");
  }
  
  public void setStatus(final String status) {
    _dbObject.put("status", status);
  }
  
  private MongoBeanList<DM_Interface> _interfaces;
  
  public List<DM_Interface> getInterfaces() {
    if(_interfaces==null)
    	_interfaces = new MongoBeanList<DM_Interface>(_dbObject, "interfaces");
    return _interfaces;
  }
  
  private MongoBeanList<DM_Process> _processes;
  
  public List<DM_Process> getProcesses() {
    if(_processes==null)
    	_processes = new MongoBeanList<DM_Process>(_dbObject, "processes");
    return _processes;
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.setReliability(0.0);
    DM_Lifetime _dM_Lifetime = new DM_Lifetime();
    final Procedure1<DM_Lifetime> _function = (DM_Lifetime it) -> {
      it.setLifetime(0.0);
      it.setUnit("");
    };
    DM_Lifetime _doubleArrow = ObjectExtensions.<DM_Lifetime>operator_doubleArrow(_dM_Lifetime, _function);
    this.setLifetime(_doubleArrow);
    String _string_1 = new String();
    this.setNodeTemplate(_string_1);
    String _string_2 = new String();
    this.setStatus(_string_2);
    this.getInterfaces();
    this.getProcesses();
  }
  
  public void setLifetime(final Procedure1<? super DM_Lifetime> initializer) {
    DM_Lifetime _dM_Lifetime = new DM_Lifetime();
    DM_Lifetime _doubleArrow = ObjectExtensions.<DM_Lifetime>operator_doubleArrow(_dM_Lifetime, initializer);
    this.setLifetime(_doubleArrow);
  }
  
  public void setStatus(final Status status) {
    String _string = status.toString();
    this.setStatus(_string);
  }
  
  public void addInterface(final Procedure1<? super DM_Interface> initializer) {
    DM_Interface _dM_Interface = new DM_Interface();
    final DM_Interface interfaceToAdd = ObjectExtensions.<DM_Interface>operator_doubleArrow(_dM_Interface, initializer);
    List<DM_Interface> _interfaces = this.getInterfaces();
    _interfaces.add(interfaceToAdd);
  }
  
  public void addProcess(final Procedure1<? super DM_Process> initializer) {
    DM_Process _dM_Process = new DM_Process();
    final DM_Process processToAdd = ObjectExtensions.<DM_Process>operator_doubleArrow(_dM_Process, initializer);
    List<DM_Process> _processes = this.getProcesses();
    _processes.add(processToAdd);
  }
  
  public void insert(final DB database) {
    final Logger LOGGER = Logger.getLogger("DM_NODE");
    final DBCollection dbCollection = database.getCollection("LiveSystem");
    DM_Node _dM_Node = new DM_Node();
    final Procedure1<DM_Node> _function = (DM_Node it) -> {
      String _name = this.getName();
      it.setName(_name);
    };
    DM_Node _doubleArrow = ObjectExtensions.<DM_Node>operator_doubleArrow(_dM_Node, _function);
    DBObject _dbObject = _doubleArrow.getDbObject();
    final DBObject result = dbCollection.findOne(_dbObject);
    boolean _equals = Objects.equal(result, null);
    if (_equals) {
      DBObject _dbObject_1 = this.getDbObject();
      dbCollection.save(_dbObject_1);
      String _name = this.getName();
      String _plus = (_name + 
        " node added to database");
      LOGGER.info(_plus);
    } else {
      String _name_1 = this.getName();
      String _plus_1 = (_name_1 + 
        " node already exists. Will NOT be updated.");
      LOGGER.info(_plus_1);
    }
  }
  
  public void update(final DBObject objectToUpdate, final DBCollection targetCollection) {
    final Logger LOGGER = Logger.getLogger("DM_NODE");
    targetCollection.remove(objectToUpdate);
    DBObject _dbObject = this.getDbObject();
    targetCollection.save(_dbObject);
    String _name = this.getName();
    String _plus = (_name + 
      " node has been updated.");
    LOGGER.info(_plus);
  }
}
