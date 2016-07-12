package edu.vanderbilt.isis.chariot.datamodel.SystemDescription;

import com.google.common.base.Objects;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_Objective;
import edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_SystemConstraint;
import edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_Time;
import java.util.Date;
import java.util.List;
import java.util.logging.Logger;
import org.bson.types.ObjectId;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;
import org.xtext.mongobeans.lib.WrappingUtil;

@SuppressWarnings("all")
public class DM_SystemDescription implements IMongoBean {
  /**
   * Creates a new DM_SystemDescription wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_SystemDescription(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_SystemDescription wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_SystemDescription() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.SystemDescription.DM_SystemDescription");
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
  
  public DM_Time getLifeTime() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("lifeTime"));
  }
  
  public void setLifeTime(final DM_Time lifeTime) {
    _dbObject.put("lifeTime", WrappingUtil.unwrap(lifeTime));
  }
  
  public DM_Time getMaintenancePeriod() {
    return WrappingUtil.wrapAndCast((DBObject) _dbObject.get("maintenancePeriod"));
  }
  
  public void setMaintenancePeriod(final DM_Time maintenancePeriod) {
    _dbObject.put("maintenancePeriod", WrappingUtil.unwrap(maintenancePeriod));
  }
  
  public double getReliabilityThreshold() {
    return (Double) _dbObject.get("reliabilityThreshold");
  }
  
  public void setReliabilityThreshold(final double reliabilityThreshold) {
    _dbObject.put("reliabilityThreshold", reliabilityThreshold);
  }
  
  public Date getStartTime() {
    return (Date) _dbObject.get("startTime");
  }
  
  public void setStartTime(final Date startTime) {
    _dbObject.put("startTime", startTime);
  }
  
  private MongoBeanList<DM_SystemConstraint> _constraints;
  
  public List<DM_SystemConstraint> getConstraints() {
    if(_constraints==null)
    	_constraints = new MongoBeanList<DM_SystemConstraint>(_dbObject, "constraints");
    return _constraints;
  }
  
  private MongoBeanList<DM_Objective> _objectives;
  
  public List<DM_Objective> getObjectives() {
    if(_objectives==null)
    	_objectives = new MongoBeanList<DM_Objective>(_dbObject, "objectives");
    return _objectives;
  }
  
  public void init() {
    String _string = new String();
    this.setName(_string);
    DM_Time _dM_Time = new DM_Time();
    final Procedure1<DM_Time> _function = (DM_Time it) -> {
      it.setTime(0.0);
      it.setUnit("");
    };
    DM_Time _doubleArrow = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time, _function);
    this.setLifeTime(_doubleArrow);
    DM_Time _dM_Time_1 = new DM_Time();
    final Procedure1<DM_Time> _function_1 = (DM_Time it) -> {
      it.setTime(0.0);
      it.setUnit("");
    };
    DM_Time _doubleArrow_1 = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time_1, _function_1);
    this.setMaintenancePeriod(_doubleArrow_1);
    this.setReliabilityThreshold(0.0);
    Date _date = new Date();
    this.setStartTime(_date);
    this.getConstraints();
    this.getObjectives();
  }
  
  public void setLifeTime(final Procedure1<? super DM_Time> initializer) {
    DM_Time _dM_Time = new DM_Time();
    DM_Time _doubleArrow = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time, initializer);
    this.setLifeTime(_doubleArrow);
  }
  
  public void setMaintenancePeriod(final Procedure1<? super DM_Time> initializer) {
    DM_Time _dM_Time = new DM_Time();
    DM_Time _doubleArrow = ObjectExtensions.<DM_Time>operator_doubleArrow(_dM_Time, initializer);
    this.setMaintenancePeriod(_doubleArrow);
  }
  
  public void addConstraint(final Procedure1<? super DM_SystemConstraint> initializer) {
    DM_SystemConstraint _dM_SystemConstraint = new DM_SystemConstraint();
    final DM_SystemConstraint constraintToAdd = ObjectExtensions.<DM_SystemConstraint>operator_doubleArrow(_dM_SystemConstraint, initializer);
    List<DM_SystemConstraint> _constraints = this.getConstraints();
    _constraints.add(constraintToAdd);
  }
  
  public void addObjective(final Procedure1<? super DM_Objective> initializer) {
    DM_Objective _dM_Objective = new DM_Objective();
    final DM_Objective objectiveToAdd = ObjectExtensions.<DM_Objective>operator_doubleArrow(_dM_Objective, initializer);
    List<DM_Objective> _objectives = this.getObjectives();
    _objectives.add(objectiveToAdd);
  }
  
  public void insert(final DB database) {
    final Logger LOGGER = Logger.getLogger("DM_SystemDescription");
    final DBCollection dbCollection = database.getCollection("SystemDescriptions");
    DM_SystemDescription _dM_SystemDescription = new DM_SystemDescription();
    final Procedure1<DM_SystemDescription> _function = (DM_SystemDescription it) -> {
      String _name = this.getName();
      it.setName(_name);
    };
    DM_SystemDescription _doubleArrow = ObjectExtensions.<DM_SystemDescription>operator_doubleArrow(_dM_SystemDescription, _function);
    DBObject _dbObject = _doubleArrow.getDbObject();
    final DBObject result = dbCollection.findOne(_dbObject);
    boolean _equals = Objects.equal(result, null);
    if (_equals) {
      DBObject _dbObject_1 = this.getDbObject();
      dbCollection.save(_dbObject_1);
      String _name = this.getName();
      String _plus = (_name + 
        " system description added to database");
      LOGGER.info(_plus);
    } else {
      String _name_1 = this.getName();
      String _plus_1 = (_name_1 + 
        " system description type already exists");
      LOGGER.info(_plus_1);
      this.update(result, dbCollection);
    }
  }
  
  public void update(final DBObject objectToUpdate, final DBCollection targetCollection) {
    final Logger LOGGER = Logger.getLogger("DM_SystemDescription");
    targetCollection.remove(objectToUpdate);
    DBObject _dbObject = this.getDbObject();
    targetCollection.save(_dbObject);
    String _name = this.getName();
    String _plus = (_name + 
      " system has been updated.");
    LOGGER.info(_plus);
  }
}
