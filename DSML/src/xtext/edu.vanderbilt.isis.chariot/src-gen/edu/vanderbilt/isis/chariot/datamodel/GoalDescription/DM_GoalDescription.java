package edu.vanderbilt.isis.chariot.datamodel.GoalDescription;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.GoalDescription.DM_Objective;
import edu.vanderbilt.isis.chariot.datamodel.GoalDescription.DM_ReplicationConstraint;
import edu.vanderbilt.isis.chariot.generator.ConfigSpaceGenerator;
import java.util.List;
import org.bson.types.ObjectId;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;

/**
 * An entity to store goal description.
 */
@SuppressWarnings("all")
public class DM_GoalDescription implements IMongoBean {
  /**
   * Creates a new DM_GoalDescription wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_GoalDescription(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_GoalDescription wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_GoalDescription() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.GoalDescription.DM_GoalDescription");
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
  
  private MongoBeanList<DM_ReplicationConstraint> _replicationConstraints;
  
  public List<DM_ReplicationConstraint> getReplicationConstraints() {
    if(_replicationConstraints==null)
    	_replicationConstraints = new MongoBeanList<DM_ReplicationConstraint>(_dbObject, "replicationConstraints");
    return _replicationConstraints;
  }
  
  private MongoBeanList<DM_Objective> _objectives;
  
  public List<DM_Objective> getObjectives() {
    if(_objectives==null)
    	_objectives = new MongoBeanList<DM_Objective>(_dbObject, "objectives");
    return _objectives;
  }
  
  /**
   * Initialization method.
   */
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.getReplicationConstraints();
    this.getObjectives();
  }
  
  /**
   * Method to add a replication constraint.
   * 
   * @param initializer	DM_ReplicationConstraint entity to be added.
   */
  public void addReplicationConstraint(final Procedure1<? super DM_ReplicationConstraint> initializer) {
    DM_ReplicationConstraint _dM_ReplicationConstraint = new DM_ReplicationConstraint();
    final DM_ReplicationConstraint constraintToAdd = ObjectExtensions.<DM_ReplicationConstraint>operator_doubleArrow(_dM_ReplicationConstraint, initializer);
    List<DM_ReplicationConstraint> _replicationConstraints = this.getReplicationConstraints();
    _replicationConstraints.add(constraintToAdd);
  }
  
  /**
   * Method to add an objective.
   * 
   * @param initializer	DM_Objective entity to be added.
   */
  public void addObjective(final Procedure1<? super DM_Objective> initializer) {
    DM_Objective _dM_Objective = new DM_Objective();
    final DM_Objective objectiveToAdd = ObjectExtensions.<DM_Objective>operator_doubleArrow(_dM_Objective, initializer);
    List<DM_Objective> _objectives = this.getObjectives();
    _objectives.add(objectiveToAdd);
  }
  
  /**
   * Method to insert a goal description entity into a database.
   * 
   * @param database	Database where the goal description entity should
   * 					be inserted.
   */
  public void insert(final DB database) {
    final DBCollection dbCollection = database.getCollection("GoalDescriptions");
    DM_GoalDescription _dM_GoalDescription = new DM_GoalDescription();
    final Procedure1<DM_GoalDescription> _function = (DM_GoalDescription it) -> {
      String _name = this.getName();
      it.setName(_name);
    };
    DM_GoalDescription _doubleArrow = ObjectExtensions.<DM_GoalDescription>operator_doubleArrow(_dM_GoalDescription, _function);
    DBObject _dbObject = _doubleArrow.getDbObject();
    final DBObject result = dbCollection.findOne(_dbObject);
    boolean _equals = Objects.equal(result, null);
    if (_equals) {
      DBObject _dbObject_1 = this.getDbObject();
      dbCollection.save(_dbObject_1);
      String _name = this.getName();
      String _plus = (_name + 
        " goal description added to database");
      ConfigSpaceGenerator.LOGGER.info(_plus);
    } else {
      String _name_1 = this.getName();
      String _plus_1 = (_name_1 + 
        " goal description type already exists");
      ConfigSpaceGenerator.LOGGER.info(_plus_1);
      this.update(result, dbCollection);
    }
  }
  
  /**
   * Method to update an existing goal description entity.
   * 
   * @param objectToUpdate	Goal description entity to update.
   * @param targetCollection	Collection where the goal description entity
   * 							is located in the database.
   */
  public void update(final DBObject objectToUpdate, final DBCollection targetCollection) {
    targetCollection.remove(objectToUpdate);
    DBObject _dbObject = this.getDbObject();
    targetCollection.save(_dbObject);
    String _name = this.getName();
    String _plus = (_name + 
      " goal has been updated.");
    ConfigSpaceGenerator.LOGGER.info(_plus);
  }
}
