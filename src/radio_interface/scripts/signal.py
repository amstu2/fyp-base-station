#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
from fabric import Connection

def getSignalStrength():
    pub = rospy.Publisher('/radio_signal', Int16, queue_size=10)
    rospy.init_node('radio_interface', anonymous=True)
    rate = rospy.Rate(2)
    ssh_connection = Connection(host="ubnt@192.168.1.201", connect_kwargs={"password":"rover"})
    while not rospy.is_shutdown():
        raw_output = ssh_connection.run('mca-status | grep signal', hide=True)
        msg = "{0.stdout}"
        signal_string = msg.format(raw_output)
        signal_split = signal_string.split('=')
        signal_int = signal_split[1]
        pub.publish(int(signal_int))
        rate.sleep()

if __name__ == '__main__':
    try:
        getSignalStrength()
    except rospy.ROSInterruptException:
        pass
