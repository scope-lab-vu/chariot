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
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.getNodeTemplates();
  }
  
  public void addNodeTemplate(final Procedure1<? super DM_NodeTemplate> initializer) {
    DM_NodeTemplate _dM_NodeTemplate = new DM_NodeTemplate();
    final DM_NodeTemplate nodeTemplateToAdd = ObjectExtensions.<DM_NodeTemplate>operator_doubleArrow(_dM_NodeTemplate, initializer);
    List<DM_NodeTemplate> _nodeTemplates = this.getNodeTemplates();
    _nodeTemplates.add(nodeTemplateToAdd);
  }
  
  /**
   * Insert new NodeCategory to 'NodeCategories' collection
   * of the given database. Check if NodeCategory already
   * exists using category name.
   * 
   * @param database - Name of the database.
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
   * Update existing NodeCategory in 'NodeCategories' collection
   * of the given database.
   * 
   * @param database - Name of the database.
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
  
  /**
   * Remove node from an existing node category.
   * 
   * @param nodeName - Name of node to be removed.
   */
  public void removeNodeTemplate(final String nodeTemplateName) {
    int index = (-1);
    int count = 0;
    List<DM_NodeTemplate> _nodeTemplates = this.getNodeTemplates();
    for (final DM_NodeTemplate nodeTemplate : _nodeTemplates) {
      {
        String _name = nodeTemplate.getName();
        boolean _equals = _name.equals(nodeTemplateName);
        if (_equals) {
          index = count;
        }
        count++;
      }
    }
    if ((index != (-1))) {
      List<DM_NodeTemplate> _nodeTemplates_1 = this.getNodeTemplates();
      _nodeTemplates_1.remove(index);
      String _name = this.getName();
      String _plus = ((nodeTemplateName + 
        " node template removed from node category ") + _name);
      ConfigSpaceGenerator.LOGGER.info(_plus);
    } else {
      String _name_1 = this.getName();
      String _plus_1 = ((nodeTemplateName + 
        " node template does not exist in node category ") + _name_1);
      ConfigSpaceGenerator.LOGGER.info(_plus_1);
    }
  }
}
