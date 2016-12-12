from setuptools import setup

setup(
    name="CHARIOTRuntimePackage",
    version="0.0.1",
    #data_files=[('/tmp', ['test.txt'])],
    packages=["chariot_runtime_libs"],
    scripts=["scripts/DeploymentManager", "scripts/ManagementEngine", "scripts/NodeMembership", "scripts/NodeMembershipWatcher", "scripts/ResourceMonitor", "scripts/SimulateNodeActivity"],
    install_requires=["pyzmq==16.0.2", "pymongo==3.4.0", "z3-solver==4.5.1", "kazoo==2.2.1", "netifaces==0.10.5", "psutil==5.0.0"]
)
