#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float64
from std_msgs.msg import UInt32
import roslib
import actionlib

import youbot_nav_msr.msg

def fineTuneClient(stateCmd):
	client=actionlib.SimpleActionClient('fineTuneNav',youbot_retrieve_msr.msg.locateblockAction)
	client.wait_for_server()
	goal = youbot_nav_msr.msg.locateblockGoal(goalState=stateCmd)
	client.send_goal(goal)
	client.wait_for_result()
	return client.get_result

if __name__ == '__main__': 
    try:
    	rospy.init_node("fineTuneClient")
	
	#chunk for the left set of blocks
#	rospy.loginfo("1st begin")
#	motion1 = fineTuneClient(4)
#	rospy.loginfo("1st success")
#	rospy.sleep(10)

	#chunk for the right set of blocks
	rospy.loginfo("1st begin")
	motion1 = fineTuneClient(3)
	rospy.loginfo("1st success")
	rospy.sleep(10)
	rospy.loginfo("2nd begin")
	motion2 = fineTuneClient(7)
	rospy.loginfo("2nd success")

	# shared code block
	rospy.loginfo("3rd begin")
	motion3 = fineTuneClient(1)
	rospy.loginfo("3rd success")
	rospy.loginfo("4th begin")
	motion4 = fineTuneClient(6)
	rospy.loginfo("4th success")
	rospy.spin()
    except rospy.ROSInterruptException: pass
