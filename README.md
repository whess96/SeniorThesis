# SeniorThesis
Repository for Alex Hsia and Will Hess's Princeton Senior Thesis

## Organization
Timeline and Todo list can be found at https://trello.com/b/piCAc8gr/thesis

Assorted non-code documents can be found at https://drive.google.com/open?id=1OhA2VEK-74bqbBii0FNRO-0e4JZKUwo7

## Dependencies
### Lightweight Communication and Marshalling (LCM)
LCM is used to send information between various parts of our setup. LCM comes with its share of dependencies as well, and installation instructions can be found at https://lcm-proj.github.io/build_instructions.html

Building the python release of LCM can be a bit temperamental, and it was necessary to update XCode and reinstall glib to get it to install and build correctly.

### PySerial
Used to send information through serial ports using python scripts. https://pyserial.readthedocs.io/en/latest/index.html

### Vicon DataStream SDK
Used to read in live positional data of the plane. Using v1.7.0.
https://www.vicon.com/downloads/utilities-and-sdk/datastream-sdk/archive/datastream-sdk-171

### Python3
This project uses Apple's v3.6.1 Python release. It is recommended that the user works within a virtual environment to ensure their Python release is compatible.
