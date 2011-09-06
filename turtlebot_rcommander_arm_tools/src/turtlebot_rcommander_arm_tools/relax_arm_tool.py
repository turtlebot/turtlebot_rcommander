import roslib; roslib.load_manifest('turtlebot_rcommander_arm_tools')
import rcommander.tool_utils as tu
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import functools as ft
import simple_arm_actions.msg as pm
import geometry_msgs.msg as gm

class RelaxArmTool(tu.ToolBase):
    def __init__(self, rcommander):
        tu.ToolBase.__init__(self, rcommander, 'relax_arm_tool', 'Relax Arm', RelaxArmState)

    def fill_property_box(self, pbox):
        formlayout = pbox.layout()
        pbox.update()

    def new_node(self, name=None):
        if name == None:
            nname = self.name + str(self.counter)
        else:
            nname = name
        return RelaxArmState(nname)
    
    def set_node_properties(self, detection_state):
      pass
      
    def Relax(self):
      pass
      
class RelaxArmState(tu.SimpleStateBase):

    def __init__(self, name):
        action = 'relax_arm'

        tu.SimpleStateBase.__init__(self, name, \
                action, pm.RelaxArmAction,
                goal_cb_str = 'ros_goal')

    def ros_goal(self, userdata, default_goal):
        return pm.RelaxArmGoal()

    def __getstate__(self):
        state = tu.SimpleStateBase.__getstate__(self)
        my_state = []
        return {'simple_state': state, 'self': my_state}

    def __setstate__(self, state):
        tu.SimpleStateBase.__setstate__(self, state['simple_state'])
        #self.frame, self.z_down, self.z_up, self.gripper_open, self.gripper_closed, self.topic = state['self']
        
