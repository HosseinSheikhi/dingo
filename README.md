# dingo
This repository includes driver and simulation packages for Clear Path Dingo Robot in ROS2.

# Note:
The main differences with official Dingo package
- The official uses ros control plugin for differential drive simulation while this package uses gazebo diff drive plugin
- The official uses ridgback force baced move plugin for omni drive simulation while this package uses planar move plugin 
- An SDF file is prepared in this package for both dingo types while the official just uses urdf files

#TODO: 

- maybe some joints are not necessary in dino-o sdf file
