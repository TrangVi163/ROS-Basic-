#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import math

class ControlMotion():
    def __init__(self):

        self.msg = Twist()
        self.msg.linear.x = 0.5
        self.msg.angular.z = 0.0

        self.pub_twist = rospy.Publisher("cmd_vel", Twist, queue_size=5)
        rospy.loginfo("Publisher set")

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.pub_twist.publish(self.msg)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('ControlMotion')
    control_motion = ControlMotion()
    control_motion.run()
