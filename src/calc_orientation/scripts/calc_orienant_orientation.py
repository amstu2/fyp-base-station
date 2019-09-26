#!/usr/bin/env python

import rospy
from  std_msgs.msg import Float64MultiArray

class Tracker:
    def __init__(self, latitude = 0.00, longitude = 0.00):
        self.latitude = latitude
        self.longitude = longitude
        self.position_is_locked = False
        self.LOCK_LIMIT = 60 
        self.lock_count = 0

    def resetLockCount(self):
        self.lock_count = 0

    def printGPSCoordinates(self):
        rospy.loginfo("\r\nAntenna Latitude: " + str(self.latitude) + "\r\nAntennna Longitude: " + str(self.longitude))

class Vehicle:
    def __init__(self, latitude = 0.00, longitude = 0.00):
        self.latitude = latitude
        self.longitude = longitude

    def printGPSCoordinates(self):
        rospy.loginfo("\r\nVehicle Latitude: " + str(self.latitude) + "\r\nVehicle Longitude: " + str(self.longitude))

def antGPSCallback(data):
    latitude_new = data.data[0]
    longitude_new = data.data[1]
    if((latitude_new == antenna.latitude) and (longitude_new == antenna.longitude)):
        antenna.lock_count += 1
        if(antenna.lock_count == antenna.LOCK_LIMIT):
            antenna.position_is_locked = True
            rospy.loginfo('Antenna position locked')
    else:
        antenna.resetLockCount
        antenna.latitude = latitude_new
        antenna.longitude = longitude_new
        rospy.loginfo('New antenna GPS coordinates established: ' + str(antenna.latitude) + ' ' + str(antenna.longitude))


def roverGPSCallback(data):
    rover.latitude = data.data[0]
    rover.longitude = data.data[1]
    rospy.loginfo('test')
    rover.printGPSCoordinates()

def calculateAntennaOrientation():
    rospy.Subscriber('ant_gps', Float64MultiArray, antGPSCallback)
    rospy.Subscriber('rover_gps', Float64MultiArray, roverGPSCallback)
    rospy.init_node('ant_orient', anonymous=True)
    rospy.loginfo(str(antenna.latitude))
    rospy.spin()

antenna = Tracker()
rover = Vehicle()
if __name__ == '__main__':
    try:
        calculateAntennaOrientation()
    except rospy.ROSInterruptException:
        pass