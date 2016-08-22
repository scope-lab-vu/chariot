package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_NodeTemplate;
import edu.vanderbilt.isis.chariot.generator.ConfigSpaceGenerator;
import java.util.List;
import org.bson.types.ObjectId;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;

/**
 * An entity to store node category.
 */
@SuppressWarnings("all")
public class DM_NodeCategory implements IMongoBean {
  /**
   * Creates a new DM_NodeCategory wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_NodeCategory(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_NodeCategory wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_NodeCategory() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_NodeCategory");
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
  
  private MongoBeanList<DM_NodeTemplate> _nodeTemplates;
  
  public List<DM_NodeTemplate> getNodeTemplates() {
    if(_nodeTemplates==null)
    	_nodeTemplates = new MongoBeanList<DM_NodeTemplate>(_dbObject, "nodeTemplates");
    return _nodeTemplates;
  }
  
  /**
   * Initialization method.
   */
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.getNodeTemplates();
  }
  
  /**
   * Method to add a node template.
   * 
   * @param initializer	DM_NodeTemplate entity to be added.
   */
  public void addNodeTemplate(final Procedure1<? super DM_NodeTemplate> initializer) {
    DM_NodeTemplate _dM_NodeTemplate = new DM_NodeTemplate();
    final DM_NodeTemplate nodeTemplateToAdd = ObjectExtensions.<DM_NodeTemplate>operator_doubleArrow(_dM_NodeTemplate, initializer);
    List<DM_NodeTemplate> _nodeTemplates = this.getNodeTemplates();
    _nodeTemplates.add(nodeTemplateToAdd);
  }
  
  /**
   * Method to insert node category entity into a database.
   * 
   * @param database	Database where the node category entity should
   * 					be inserted.
   */
  public void insert(final DB database) {
    final DBCollection dbCollection = database.getCollection("NodeCategories");
    DM_NodeCategory _dM_NodeCategory = new DM_NodeCategory();
    final Procedure1<DM_NodeCategory> _function = (DM_NodeCategory it) -> {
      String _name = this.getName();
      it.setName(_name);
    };
    DM_NodeCategory _doubleArrow = ObjectExtensions.<DM_NodeCategory>operator_doubleArrow(_dM_NodeCategory, _function);
    DBObject _dbObject = _doubleArrow.getDbObject();
    final DBObject result = dbCollection.findOne(_dbObject);
    boolean _equals = Objects.equal(result, null);
    if (_equals) {
      DBObject _dbObject_1 = this.getDbObject();
      dbCollection.save(_dbObject_1);
      String _name = this.getName();
      String _plus = (_name + 
        " node category added to database");
      ConfigSpaceGenerator.LOGGER.info(_plus);
    } else {
      String _name_1 = this.getName();
      String _plus_1 = (_name_1 + 
        " node category already exists. Trying to update.");
      ConfigSpaceGenerator.LOGGER.info(_plus_1);
      this.update(result, dbCollection);
    }
  }
  
  /**
   * Method to update an existing node category entity.
   * 
   * @param objectToUpdate	Node category entity to update.
   * @param targetCollection	Collection where the node category entity
   * 							is located in the database.
   */
  public void update(final DBObject objectToUpdate, final DBCollection targetCollection) {
    targetCollection.remove(objectToUpdate);
    DBObject _dbObject = this.getDbObject();
    targetCollection.save(_dbObject);
    String _name = this.getName();
    String _plus = (_name + 
      " node category has been updated.");
    ConfigSpaceGenerator.LOGGER.info(_plus);
  }
}
