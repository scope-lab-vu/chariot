package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Artifact;
import edu.vanderbilt.isis.chariot.datamodel.Status;
import java.util.List;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;

/**
 * An entity to store device.
 */
@SuppressWarnings("all")
public class DM_Device implements IMongoBean {
  /**
   * Creates a new DM_Device wrapping the given {@link com.mongodb.DBObject}.
   */
  public DM_Device(final DBObject dbObject) {
    this._dbObject = dbObject;
  }
  
  /**
   * Creates a new DM_Device wrapping a new {@link com.mongodb.BasicDBObject}.
   */
  public DM_Device() {
    _dbObject = new BasicDBObject();
    _dbObject.put(JAVA_CLASS_KEY, "edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Device");
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
  
  private MongoBeanList<DM_Artifact> _artifacts;
  
  public List<DM_Artifact> getArtifacts() {
    if(_artifacts==null)
    	_artifacts = new MongoBeanList<DM_Artifact>(_dbObject, "artifacts");
    return _artifacts;
  }
  
  public String getStatus() {
    return (String) _dbObject.get("status");
  }
  
  public void setStatus(final String status) {
    _dbObject.put("status", status);
  }
  
  /**
   * Initialization method.
   */
  public void init() {
    String _string = new String();
    this.setName(_string);
    this.getArtifacts();
    String _string_1 = new String();
    this.setStatus(_string_1);
  }
  
  /**
   * Method to add an artifact.
   * 
   * @param initializer	DM_Artifact entity to be added.
   */
  public void addArtifact(final Procedure1<? super DM_Artifact> initializer) {
    DM_Artifact _dM_Artifact = new DM_Artifact();
    final DM_Artifact artifactToAdd = ObjectExtensions.<DM_Artifact>operator_doubleArrow(_dM_Artifact, initializer);
    List<DM_Artifact> _artifacts = this.getArtifacts();
    _artifacts.add(artifactToAdd);
  }
  
  /**
   * Method to set device status.
   * 
   * @param status	Device status.
   */
  public void setStatus(final Status status) {
    String _string = status.toString();
    this.setStatus(_string);
  }
}
