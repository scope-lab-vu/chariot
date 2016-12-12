[![Build Status](https://travis-ci.org/visor-vu/chariot.svg?branch=master)](https://travis-ci.org/visor-vu/chariot)

# Chariot

CHARIOT is a holistic solution that facilitates design, development, and management of [extensible CPS](http://etd.library.vbe.proxy.library.vanderbilt.edu/available/etd-11172016-154749/unrestricted/Pradhan.pdf). CHARIOT consists of different entities that can be classified into three layers:

<img src="https://github.com/visor-vu/chariot/blob/master/LayeredOverview.png" width="50%" height="50%"/>

- Domain-specific modeling language: CHARIOT-ML (Modeling Language) is a Domain-Specific Modeling Language (DSML) that can be used to model applications and systems. Applications are modeled as software components that provide functionalities. Systems are modeled as composition of one or more functionalities. CHARIOT-ML is a design-time tool.
- Generic component model: CHARIOT implements a novel component model that, unlike any existing component models, is middleware agnostic. At its very core, this component model relies on the design principle that a software component should have a clean separation-of-concerns between its computation and communication logic. This component model is part of both design-time (modeling application components) and runtime (execution of application components) aspect of CHARIOT.
- Autonomous resilience loop: Runtime aspect of CHARIOT also includes different entities that constitutes an autonomous resilience loop. The management infrastructure is responsible for managing a platform, whereas, the monitoring infrastructure is responsible for monitoring resources of the platform for failures and anomalies. Finally, the resilience infrastructure is responsible for determining how to resolve failures and anomalies detected by the aforementioned monitoring infrastructure. As shown in the figure below, these entities form a closed sense-plan-act loop to make sure system required functionalities provided by different applications are maintained for as long as possible.

Chariot uses the following other open source projects

- Xtext
- Z3

For further information please see http://chariot.isis.vanderbilt.edu/

# Examples

Examples are available at https://github.com/visor-vu/chariot-examples
