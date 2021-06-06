#! /usr/bin/env python

import rospy
sonars = []
from sensor_msgs.msg import Range
class ReadSonar():
    def __init__(self):
        self.range_left = 0
        self.range_center = 0
        self.range_right = 0

        self.sub_left = rospy.Subscriber("/robot/sonar_sensor/link_sonar_left", Range, self.update_rangeL)
        self.sub_center = rospy.Subscriber("/robot/sonar_sensor/link_sonar_center", Range, self.update_rangeC)
        self.sub_right = rospy.Subscriber("/robot/sonar_sensor/link_sonar_right", Range, self.update_rangeR)
        rospy.loginfo("Subscribers set")

    def update_rangeL(self, msg):
        self.range_left = msg.range 
    def update_rangeC(self, msg):
        self.range_center = msg.range
    def update_rangeR(self, msg):
        self.range_right = msg.range

    def run(self):
        rate = rospy.Rate(5)
        while not rospy.is_shutdown():
            sonars = [
                self.range_left,
                self.range_center,
                self.range_right,
            ]
            rospy.loginfo(sonars)
            rate.sleep()
if __name__ == '__main__':
    rospy.init_node('read sensor')
    read_sonar = ReadSonar()
    read_sonar.run()
