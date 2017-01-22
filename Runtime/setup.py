from setuptools import setup

setup(
    name="chariot-runtime",
    version="0.0.5",
    author="visor-vu",
    author_email="visorvu@gmail.com",
    description="CHARIOT Runtime Package (Beta)",
    license="MIT",
    url="https://github.com/visor-vu/chariot",
    data_files=[("/etc/chariot/", ["chariot.conf"]), ("/etc/init.d/", ["init_scripts/chariot-dm", "init_scripts/chariot-nm", "init_scripts/chariot-nmw"])],
    packages=["chariot_runtime_libs"],
    scripts=["scripts/chariot-dm", "scripts/chariot-me", "scripts/chariot-nm", "scripts/chariot-nmw", "scripts/chariot-rm", "scripts/chariot-sna"],
    install_requires=["pyzmq==16.0.2", "pymongo==3.4.0", "z3-solver==4.5.1", "kazoo==2.2.1", "netifaces==0.10.5", "psutil==5.0.0"],
    zip_safe=False
)
