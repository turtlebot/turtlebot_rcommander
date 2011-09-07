import roslib; roslib.load_manifest('turtlebot_rcommander_arm_tools')
import rcommander.tool_utils as tu
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import functools as ft
import turtlebot_block_manipulation.msg as pm

class InteractiveBlockManipulationTool(tu.ToolBase):

    DEFAULT_TEXT = 'arm_base_link'

    def __init__(self, rcommander):
        tu.ToolBase.__init__(self, rcommander, 'interactive_block_manipulation_tool', 'Interactive Block Manipulation', InteractiveBlockManipulationState)

    def fill_property_box(self, pbox):
        formlayout = pbox.layout()
        self.frame = QLineEdit(pbox)
        self.frame.setText(InteractiveBlockManipulationTool.DEFAULT_TEXT)
        self.block_box = tu.SliderBox(pbox, 0.03, 0.1, 0., 1000, 'block_size', units='m')

        formlayout.addRow('&Detection Frame', self.frame)
        formlayout.addRow('&Block Size', self.block_box.container)
        pbox.update()

    def new_node(self, name=None):
        frame = str(self.frame.text())
        block_size = self.block_box.value()

        if name == None:
            nname = self.name + str(self.counter)
        else:
            nname = name
        return InteractiveBlockManipulationState(nname, frame, block_size)
    
    def set_node_properties(self, detection_state):
        self.frame.setText(detection_state.frame)
        self.block_box.set_value(detection_state.block_size)

    def reset(self):
        self.frame.setText(InteractiveBlockManipulationTool.DEFAULT_TEXT)
        self.block_box.set_value(0.03)

class InteractiveBlockManipulationState(tu.SimpleStateBase):

    def __init__(self, name, frame, block_size):
        action = 'interactive_manipulation'

        tu.SimpleStateBase.__init__(self, name, \
                action, pm.InteractiveBlockManipulationAction,
                goal_cb_str = 'ros_goal')

        self.frame = frame
        self.block_size = block_size

    def ros_goal(self, userdata, default_goal):
        #import time
        #while True:
        #    time.sleep(.01)
        return pm.InteractiveBlockManipulationGoal(self.frame, self.block_size)

    def __getstate__(self):
        state = tu.SimpleStateBase.__getstate__(self)
        my_state = [self.frame, self.block_size]
        return {'simple_state': state, 'self': my_state}

    def __setstate__(self, state):
        tu.SimpleStateBase.__setstate__(self, state['simple_state'])
        self.frame, self.block_size = state['self']
