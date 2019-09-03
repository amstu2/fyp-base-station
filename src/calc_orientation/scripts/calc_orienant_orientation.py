#!/usr/bin/env python

import rospy
from  std_msgs.msg import Float64MultiArray

def antGPSCallback(data):
    rospy.loginfo('new antenna gps info' + str(data.data[0]))

def roverGPSCallback(data):
    rospy.loginfo('new rover gps info')

def calculateAntennaOrientation():
    rospy.init_node('ant_orient', anonymous=True)
    rospy.Subscriber('ant_gps', Float64MultiArray, antGPSCallback)
    rospy.Subscriber('rover_gps', Float64MultiArray, roverGPSCallback)
    rospy.spin()

if __name__ == '__main__':
    try:
        calculateAntennaOrientation()
    except rospy.ROSInterruptException:
        pass