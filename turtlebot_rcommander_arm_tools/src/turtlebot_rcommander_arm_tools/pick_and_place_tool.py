import roslib; roslib.load_manifest('turtlebot_rcommander_arm_tools')
import rcommander.tool_utils as tu
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import functools as ft
import turtlebot_block_manipulation.msg as pm
import geometry_msgs.msg as gm

class PickAndPlaceTool(tu.ToolBase):

    DEFAULT_FRAME = 'arm_base_link'
    DEFAULT_TOPIC = '/pick_and_place'

    def __init__(self, rcommander):
        tu.ToolBase.__init__(self, rcommander, 'pick_and_place_tool', 'Pick and Place', PickAndPlaceState)

    def fill_property_box(self, pbox):
        formlayout = pbox.layout()
        self.frame = QLineEdit(pbox)
        self.frame.setText(PickAndPlaceTool.DEFAULT_FRAME)
        self.z_up_box = tu.SliderBox(pbox, 0.12, 0.25, -0.15, 1000, 'z_up', units='m')
        self.g_open_box = tu.SliderBox(pbox, 0.042, 0.1, 0.0, 1000, 'g_open', units='m')
        self.g_closed_box = tu.SliderBox(pbox, 0.024, 0.1, 0.0, 1000, 'g_closed', units='m')
        self.topic = QLineEdit(pbox)
        self.topic.setText(PickAndPlaceTool.DEFAULT_TOPIC)

        formlayout.addRow('&Arm Frame', self.frame)
        formlayout.addRow('&Z Up', self.z_up_box.container)
        formlayout.addRow('&Gripper Open', self.g_open_box.container)
        formlayout.addRow('&Gripper Closed', self.g_closed_box.container)
        formlayout.addRow('&Subscription Topic', self.topic)
        pbox.update()

    def new_node(self, name=None):
        frame = str(self.frame.text())
        z_up = self.z_up_box.value()
        gripper_open = self.g_open_box.value()
        gripper_closed = self.g_closed_box.value()
        topic = str(self.topic.text())

        if name == None:
            nname = self.name + str(self.counter)
        else:
            nname = name
        return PickAndPlaceState(nname, frame, z_up, gripper_open, gripper_closed, topic)
    
    def set_node_properties(self, detection_state):
        self.frame.setText(detection_state.frame)
        self.z_up_box.set_value(detection_state.z_up)
        self.g_open_box.set_value(detection_state.gripper_open)
        self.g_closed_box.set_value(detection_state.gripper_closed)
        self.topic.setText(detection_state.topic)

    def reset(self):
        self.frame.setText(PickAndPlaceTool.DEFAULT_FRAME)
        self.z_up_box.set_value(0.12)
        self.g_open_box.set_value(0.042)
        self.g_closed_box.set_value(0.024)
        self.topic.setText(PickAndPlaceTool.DEFAULT_TOPIC)

class PickAndPlaceState(tu.SimpleStateBase):

    def __init__(self, name, frame, z_up, gripper_open, gripper_closed, topic):
        action = 'pick_and_place'

        tu.SimpleStateBase.__init__(self, name, \
                action, pm.PickAndPlaceAction,
                goal_cb_str = 'ros_goal')

        self.frame = frame
        self.z_up = z_up
        self.gripper_open = gripper_open
        self.gripper_closed = gripper_closed
        self.topic = topic

    def ros_goal(self, userdata, default_goal):
        return pm.PickAndPlaceGoal(self.frame, self.z_up, self.gripper_open, self.gripper_closed, gm.Pose(), gm.Pose(), self.topic)

    def __getstate__(self):
        state = tu.SimpleStateBase.__getstate__(self)
        my_state = [self.frame, self.z_up, self.gripper_open, self.gripper_closed, self.topic]
        return {'simple_state': state, 'self': my_state}

    def __setstate__(self, state):
        tu.SimpleStateBase.__setstate__(self, state['simple_state'])
        self.frame, self.z_up, self.gripper_open, self.gripper_closed, self.topic = state['self']
        
