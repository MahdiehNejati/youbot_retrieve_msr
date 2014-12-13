#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float64
from std_msgs.msg import UInt32
import roslib
import actionlib

import youbot_retrieve_msr.msg

def stateManager():

	rospy.loginfo("1st begin")
	motion1 = fineTuneClient(4)
	rospy.loginfo("1st success")
	rospy.sleep(10)
	
#	rospy.loginfo("1st begin")
#	motion1 = fineTuneClient(3)
#	rospy.loginfo("1st success")
#	rospy.sleep(10)
#	rospy.loginfo("2nd begin")
#	motion2 = fineTuneClient(7)
#	rospy.loginfo("2nd success")

	# shared code block
	rospy.loginfo("3rd begin")
	motion3 = fineTuneClient(1)
	rospy.loginfo("3rd success")
	rospy.loginfo("4th begin")
	motion4 = fineTuneClient(6)
	rospy.loginfo("4th success")
	rospy.loginfo("4.5 begin")
	motion3 = fineTuneClient(1)
	rospy.loginfo("4.5 success")


		
	grabBlock = graspClient(1)
	
		
	
	atHome = fineTuneClient(5) 
	rospy.wait(5)
		
	dropped = graspClient(2)		
	#If succesfully at home, wait for new command. 
	

def fineTuneClient(stateCmd):
	client=actionlib.SimpleActionClient('fineTuneNav',youbot_retrieve_msr.msg.locateblockAction)
	client.wait_for_server()
	goal = youbot_retrieve_msr.msg.locateblockGoal(goalState=stateCmd)
	client.send_goal(goal)
	client.wait_for_result()
	rospy.loginfo("got here")
	outcome = client.get_result
	return outcome


def graspClient(stateCmd):
	client = actionlib.SimpleActionClient('graspObject', youbot_retrieve_msr.msg.graspblockAction)
	client.wait_for_server()
	goal = youbot_retrieve_msr.msg.graspblockGoal(goalState=stateCmd)
	client.send_goal(goal)
	client.wait_for_result()
	rospy.loginfo("picked up object")
	outcome = client.get_result
	return outcome



if __name__ == '__main__': 
    try:
    	rospy.init_node("retrieveClient")
    	stateManager()
	rospy.spin()
    except rospy.ROSInterruptException: pass
