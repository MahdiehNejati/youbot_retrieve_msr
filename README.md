This package combines navigation and grasping for the KUKA youBot to grab a cube. 

Introduction
============

This is a working demo for the KUKA youbot. The youBot navigates to a designated object, aligns itself to a fine tuned location, grabs the cube and returns to base. 

This package combines these two packages:

1. [youbot_nav_msr](https://github.com/jihoonkimMSR/youbot_nav_msr)

2. [youbot_grasp_msr](https://github.com/mattmongeon/youbot_grasp_msr)


Dependencies
============

The package also relies on the following packages, installable from apt-get in Hydro. 

1. [ROS navigation stack](http://wiki.ros.org/navigation)

2. [eband_local_planner](http://wiki.ros.org/eband_local_planner)

3. [youbot_driver](https://github.com/youbot/youbot_driver)

4. [hokuyo_node](http://wiki.ros.org/hokuyo_node)

5.  [youbot_driver_ros_interface](https://github.com/youbot/youbot_driver_ros_interface)


The following dependancies are clonable via github:

6. [hrl-kdl](https://github.com/gt-ros-pkg/hrl-kdl)

7. [urdfdom](https://github.com/ros/urdfdom)

8. [brics_actuator](http://wiki.ros.org/brics_actuator) ( The brics messages are required by the hrl-kdl) 


Running the Demo
================

Currently, the files in this folder are calibrated to work in a specific lab environment. It uses the map for that particular space, so the map should be replaced with a customized map of its environment. In addition, while the setup requirements in this particular space do not have to be extremely precise, reliable results are guaranteed by the following set up for use within Northwestern University's D110 lab:

Align the back wheels of the youBot to be roughly on the two small pieces of tape within the closed off area.
Place two stacks of 3 blocks on the two green pluses in the closed off area.
Place a small block (block to grasp) inside the small marked off red square.

```bash
roslaunch youbot_retrieve_msr nav_and_grasp.launch 
rosrun youbot_retrieve_msr youbot_grasping.py
rosrun youbot_retrieve_msr fineTuneActionServ_odom.py
rosrun youbot_retrieve_msr retrieveClient.py
```
