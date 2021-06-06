#! /usr/bin/env python

import rospy

from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
#from std_srvs.srv import *

import math
sonars = []

class FollowWall():

    def __init__(self):
 
        self.state_ = 0
        self.d_hit = 0.2
        self.d = 0.5
        self.state_dict_ = {
            0: 'find the wall',
            1: 'turn left',
            2: 'follow the wall',
        }
        self.range_left = 0
        self.range_center = 0
        self.range_right = 0

        self.msg = Twist()
        self.linear_x = 0
        self.angular_z = 0

        self.sub_left = rospy.Subscriber("/robot/sonar_sensor/link_sonar_left", Range, self.update_rangeL)
        self.sub_center = rospy.Subscriber("/robot/sonar_sensor/link_sonar_center", Range, self.update_rangeC)
        self.sub_right = rospy.Subscriber("/robot/sonar_sensor/link_sonar_right", Range, self.update_rangeR)

        rospy.loginfo("Subscribers set")
        self.pub_twist = rospy.Publisher("cmd_vel", Twist, queue_size=5)
        rospy.loginfo("Publisher set")
#        self.srv = rospy.Service('wall_follower_switch', SetBool, self.wall_follower_switch)

    def update_rangeL(self, msg):
        self.range_left = msg.range 
    def update_rangeC(self, msg):
        self.range_center = msg.range
    def update_rangeR(self, msg):
        self.range_right = msg.range
    def change_state(self, state):
        if state is not self.state_:
            print 'Wall follower - [%s] - %s' % (state, self.state_dict_[state])
            self.state_ = state
    def take_action(self,regions):
        
        state_description = ''
        
        if regions[0] > self.d and regions[1] > self.d and regions[2] > self.d:
            self.state_description = 'case 1 - nothing'
            self.change_state(0)
        elif regions[1] > self.d and regions[2] < self.d:
            self.state_description = 'case 2 - right'
            self.change_state(2)       
        else:
            self.change_state(1)

#        rospy.loginfo(self.state_description)
        
    def find_wall(self,regions):
        self.msg.linear.x = 0.4
        self.msg.angular.z = -1.0
        rospy.loginfo("find wall")
        return self.msg
#        rospy.sleep(0.15)

    def turn_left(self,regions):
        self.msg.angular.z =1.7
        self.msg.linear.x = 0.4
        rospy.loginfo("turn left")
        return self.msg
#        rospy.sleep(0.15)

    def follow_the_wall(self,regions):     
        if regions[2] < self.d_hit:
            self.msg.angular.z = 1.0
            self.msg.linear.x = 0.4
#           self.msg.linear.x = 0.2
        elif regions[2] > (self.d_hit + self.d)/2:
 #           rospy.loginfo((self.d_hit + self.d)/2)
            self.msg.angular.z = -1.0
            self.msg.linear.x = 0.4
        else:
            self.msg.angular.z = 0.0
            self.msg.linear.x = 0.4
        rospy.loginfo("follow wall")
        return self.msg
#        rospy.sleep(0.15)

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            sonars = [
                self.range_left,
                self.range_center,
                self.range_right,
            ]
            rospy.loginfo(sonars)
            self.take_action(sonars)
 #           if not active_:
 #               rate.sleep()
 #               continue
            
            if self.state_ == 0:
                self.msg = self.find_wall(sonars)
            elif self.state_ == 1:
                self.msg = self.turn_left(sonars)
            elif self.state_ == 2:
                self.msg = self.follow_the_wall(sonars)
 #               pass
            else:
                rospy.logerr('Unknown state!')
            
            self.pub_twist.publish(self.msg)
            rate.sleep()
if __name__ == '__main__':
    rospy.init_node('reading_sonar')
    follow_wall = FollowWall()
    follow_wall.run()
