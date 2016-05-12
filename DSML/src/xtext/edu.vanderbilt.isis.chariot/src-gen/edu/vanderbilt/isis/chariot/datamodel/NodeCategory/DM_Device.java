package edu.vanderbilt.isis.chariot.datamodel.NodeCategory;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import edu.vanderbilt.isis.chariot.datamodel.Node.DM_Lifetime;
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_Artifact;
import edu.vanderbilt.isis.chariot.datamodel.Status;
import java.util.List;
import org.eclipse.xtext.xbase.lib.ObjectExtensions;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.xtext.mongobeans.lib.IMongoBean;
import org.xtext.mongobeans.lib.MongoBeanList;
import org.xtext.mongobeans.lib.WrappingUtil;

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
    this.getArtifacts();
    String _string_1 = new String();
    this.setStatus(_string_1);
  }
  
  public void setLifetime(final Procedure1<? super DM_Lifetime> initializer) {
    DM_Lifetime _dM_Lifetime = new DM_Lifetime();
    DM_Lifetime _doubleArrow = ObjectExtensions.<DM_Lifetime>operator_doubleArrow(_dM_Lifetime, initializer);
    this.setLifetime(_doubleArrow);
  }
  
  public void addArtifact(final Procedure1<? super DM_Artifact> initializer) {
    DM_Artifact _dM_Artifact = new DM_Artifact();
    final DM_Artifact artifactToAdd = ObjectExtensions.<DM_Artifact>operator_doubleArrow(_dM_Artifact, initializer);
    List<DM_Artifact> _artifacts = this.getArtifacts();
    _artifacts.add(artifactToAdd);
  }
  
  public void setStatus(final Status status) {
    String _string = status.toString();
    this.setStatus(_string);
  }
}
