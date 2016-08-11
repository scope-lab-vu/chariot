package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Artifact;
import edu.vanderbilt.isis.chariot.datamodel.Status;
import edu.vanderbilt.isis.chariot.generator.ConfigSpaceGenerator;
import java.util.List;
import org.eclipse.xtext.xbase.lib.Functions.Function1;
import org.eclipse.xtext.xbase.lib.ListExtensions;
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
    final Function1<DM_Artifact, String> _function = (DM_Artifact it) -> {
      return it.getName();
    };
    final List<String> curArtifacts = ListExtensions.<DM_Artifact, String>map(_artifacts, _function);
    String _name = artifactToAdd.getName();
    boolean _contains = curArtifacts.contains(_name);
    boolean _not = (!_contains);
    if (_not) {
      List<DM_Artifact> _artifacts_1 = this.getArtifacts();
      _artifacts_1.add(artifactToAdd);
    } else {
      String _name_1 = artifactToAdd.getName();
      String _plus = (_name_1 + 
        " artifact already exists in device ");
      String _name_2 = this.getName();
      String _plus_1 = (_plus + _name_2);
      ConfigSpaceGenerator.LOGGER.info(_plus_1);
    }
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
