from setuptools import setup

setup(
    name="chariot-runtime",
    version="0.0.5",
    author="visor-vu",
    author_email="visorvu@gmail.com",
    description="CHARIOT Runtime Package (Beta)",
    license="MIT",
    url="https://github.com/visor-vu/chariot",
    #data_files=[("/etc/chariot/", ["chariot.conf"]), ("/etc/init.d/", ["init_scripts/chariot-dm", "init_scripts/chariot-nm", "init_scripts/chariot-nmw"])],
    data_files=[("/etc/chariot/", ["chariot.conf"]), ("/etc/systemd/system/", ["systemd_scripts/chariot-dm.service", "systemd_scripts/chariot-nm.service", "systemd_scripts/chariot-nmw.service"])],
    #data_files=[("/etc/chariot/", ["chariot.conf"]), ("/etc/systemd/system/", ["systemd_scripts/chariot-nm.service"])],
    packages=["chariot_runtime_libs", "libs"],
    scripts=["scripts/chariot-dm", "scripts/chariot-me", "scripts/chariot-nm", "scripts/chariot-nmw", "scripts/chariot-rm", "scripts/chariot-sna"],
    install_requires=["pyzmq==16.0.2", "pymongo==3.4.0", "kazoo==2.2.1", "netifaces==0.10.5", "psutil==5.0.0"],
    zip_safe=False
)
