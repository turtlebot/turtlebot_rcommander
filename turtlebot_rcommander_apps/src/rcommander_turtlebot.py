#!/usr/bin/python
import roslib; roslib.load_manifest('rcommander_turtlebot')
import rcommander.rcommander as rc
import rospy
import tf 

rospy.init_node('rcommander', anonymous=True)
tf = tf.TransformListener()
rc.run(None, tf, 'turtlebot')
