import roslib; roslib.load_manifest('turtlebot_rcommander_arm_tools')
import rcommander.tool_utils as tu
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import functools as ft
import turtlebot_block_manipulation.msg as pm

class BlockDetectionTool(tu.ToolBase):

    DEFAULT_TEXT = 'arm_base_link'

    def __init__(self, rcommander):
        tu.ToolBase.__init__(self, rcommander, 'block_detection_tool', 'Block Detection', BlockDetectionState)

    def fill_property_box(self, pbox):
        formlayout = pbox.layout()
        self.frame = QLineEdit(pbox)
        self.frame.setText(BlockDetectionTool.DEFAULT_TEXT)
        self.table_box = tu.SliderBox(pbox, -0.05, 0.25, -0.15, 1000, 'table_height', units='m')
        self.block_box = tu.SliderBox(pbox, 0.03, 0.1, 0., 1000, 'block_size', units='m')

        formlayout.addRow('&Detection Frame', self.frame)
        formlayout.addRow('&Table Height', self.table_box.container)
        formlayout.addRow('&Block Size', self.block_box.container)
        pbox.update()

    def new_node(self, name=None):
        frame = str(self.frame.text())
        table_height = self.table_box.value()
        block_size = self.block_box.value()

        if name == None:
            nname = self.name + str(self.counter)
        else:
            nname = name
        return BlockDetectionState(nname, frame, table_height, block_size)
    
    def set_node_properties(self, detection_state):
        self.frame.setText(detection_state.frame)
        self.table_box.set_value(detection_state.table_height)
        self.block_box.set_value(detection_state.block_size)

    def reset(self):
        self.frame.setText(BlockDetectionTool.DEFAULT_TEXT)
        self.table_box.set_value(-0.05)
        self.block_box.set_value(0.03)

class BlockDetectionState(tu.SimpleStateBase):

    def __init__(self, name, frame, table_height, block_size):
        action = 'block_detection'

        tu.SimpleStateBase.__init__(self, name, \
                action, pm.BlockDetectionAction,
                goal_cb_str = 'ros_goal')

        self.frame = frame
        self.table_height = table_height
        self.block_size = block_size

    def ros_goal(self, userdata, default_goal):
        #import time
        #while True:
        #    time.sleep(.01)
        return pm.BlockDetectionGoal(self.frame, self.table_height, self.block_size)

    def __getstate__(self):
        state = tu.SimpleStateBase.__getstate__(self)
        my_state = [self.frame, self.table_height, self.block_size]
        return {'simple_state': state, 'self': my_state}

    def __setstate__(self, state):
        tu.SimpleStateBase.__setstate__(self, state['simple_state'])
        self.frame, self.table_height, self.block_size = state['self']
