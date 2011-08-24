#!/usr/bin/python
import roslib; roslib.load_manifest('turtlebot_rcommander_apps')
import rcommander.rcommander as rc
import rospy
import tf 

rospy.init_node('rcommander', anonymous=True)
tf = tf.TransformListener()
rc.run(None, tf, 'turtlebot')
