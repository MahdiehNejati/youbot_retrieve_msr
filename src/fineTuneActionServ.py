#!/usr/bin/env python

import rospy
import math
import numpy as np
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import UInt32
from geometry_msgs.msg import Quaternion

import roslib
import actionlib

import youbot_retrieve_msr.msg

cubeThresh = 0.5

scan = LaserScan()

def scanUpdate(lScan):
	global scan
	scan = lScan

class fineTuneServer(object):
	global scan

	_result =youbot_retrieve_msr.msg.locateblockResult()

	def __init__(self):
		self._as = actionlib.SimpleActionServer('fineTuneNav',youbot_retrieve_msr.msg.locateblockAction, execute_cb=self.execute_cb, auto_start=False)
		self._as.start()

	def execute_cb(self, goal):
		goalReached=0
		rate = rospy.Rate(1.0)
		
		# goal==1 means do the fine tuning action
		if (goal.goalState==1):
			idealTurn = Twist()
			targetAngle=0.0

			robotController = rospy.Publisher('cmd_vel',Twist,queue_size=10)

			while (not rospy.is_shutdown()) and (goalReached == 0):
				edgeCounter = 0		
				for i in range(len(scan.ranges)):
					if (i>0) and (abs(scan.ranges[i] < cubeThresh)):
						if (scan.ranges[i-1]-scan.ranges[i]) > 0.5:
							firstEdgei = i
							rospy.loginfo("first edge")
							firstEdgeAngle = scan.angle_min + i*scan.angle_increment
							edgeCounter = edgeCounter + 1
						elif (scan.ranges[i+1]-scan.ranges[i]) > 0.5:
							secondEdgei = i
							rospy.loginfo("second edge")
							secondEdgeAngle = scan.angle_min + i*scan.angle_increment
							edgeCounter = edgeCounter + 1
				if (edgeCounter == 2):
					blockCenterAngle = (firstEdgeAngle+secondEdgeAngle)/2.0
	
					if (blockCenterAngle > 0) and (abs(blockCenterAngle) > np.pi/50):
						idealTurn.angular.z = 0.05
						rospy.loginfo("turn left")
					elif (blockCenterAngle < 0) and (abs(blockCenterAngle) > np.pi/50):
						idealTurn.angular.z = -0.05
						rospy.loginfo("turn right")
					else:
						idealTurn.angular.z = 0.0
						goalReached = 1
						rospy.loginfo("centered")
				else:
					rospy.loginfo("no block center calculated")
					not_norm_w = 0.0
			
				rospy.loginfo(idealTurn.angular.z)
				rospy.loginfo(edgeCounter)
			
				robotController.publish(idealTurn)
				rate.sleep()
		# if the goal is anything else, move the base forward a little
		else:
			robotController2 = rospy.Publisher('move_base_simple/goal',PoseStamped,queue_size=10,latch=True)
			pose = PoseStamped()
			pose.header.stamp = rospy.Time.now()
			pose.header.frame_id = "odom"
			pose.pose.position.x=0.0
			pose.pose.position.y=0.0
			pose.pose.position.z=0.0
			q = np.array([0,0,1,np.pi])
			qn = q/np.linalg.norm(q)
			pose.pose.orientation=Quaternion(*qn)

			print pose			
			robotController2.publish(pose)		
			rospy.loginfo("pose should have published")

			self._result.successOrNot=1
			goalReached=1

		if (goalReached):
			self._result.successOrNot=1
			rospy.loginfo("action success")
			self._as.set_succeeded(self._result)
		else:
			self._result.successOrNot=0

if __name__=='__main__':
	rospy.init_node('fineTuneServer')
	rospy.Subscriber("scan",LaserScan,scanUpdate)
	fineTuneServer()
	rospy.spin()













