#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
from fabric import Connection

def getSignalStrength():
    pub = rospy.Publisher('/radio_signal', Int16, queue_size=10)
    pub2 = rospy.Publisher('/radio_tx_rate', Int16, queue_size=10)

    rospy.init_node('radio_interface', anonymous=True)
    rate = rospy.Rate(2)
    ssh_connection = Connection(host="ubnt@192.168.1.201", connect_kwargs={"password":"rover"})
    while not rospy.is_shutdown():
        raw_output = ssh_connection.run('mca-status | grep -Ei "signal|TxRate"', hide=True)
        msg = "{0.stdout}"
        signal_string = msg.format(raw_output)
        initial_split = signal_string.split('=')
        signal_split = initial_split[1].split('\r')[0]
        tx_split = initial_split[2].split('\r')[0]

        pub.publish(int(signal_split))
        pub2.publish(int(float(tx_split)))
        rate.sleep()

if __name__ == '__main__':
    try:
        getSignalStrength()
    except rospy.ROSInterruptException:
        pass
