import roslib; roslib.load_manifest('rcommander_turtlebot')
import rcommander.tool_utils as tu
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
#import pr2_common_action_msgs.msg as ca 
import functools as ft
#import pr2_controllers_msgs.msg as pm
import turtlebot_actions.msg as pm

class TurtlebotMoveTool(tu.ToolBase):

    def __init__(self, rcommander):
        tu.ToolBase.__init__(self, rcommander, 'turtlebot_move', 'Turtlebot Move', TurtlebotMoveState)

    def fill_property_box(self, pbox):
        formlayout = pbox.layout()
        #Left or right
        #self.radio_boxes, self.radio_buttons = tu.make_radio_box(pbox, ['Left', 'Right'], 'gripper_arm')
        #Opening distance
        self.forward_box = tu.SliderBox(pbox, 0., 10., 0., 0., 'forward', units='m')
        #Effort
        self.turn_box = tu.SliderBox(pbox, -3.14, 3.14, 0., 0., 'turn', units='rad')

        #formlayout.addRow('&Side', self.radio_boxes)
        formlayout.addRow('&Move Forward', self.forward_box.container)
        formlayout.addRow('&Turn', self.turn_box.container)
        pbox.update()

    def new_node(self, name=None):
        #selected_arm = None
        #for r in self.radio_buttons:
        #    if r.isChecked():
        #        selected_arm = str(r.text()).lower()
        #if selected_arm == None:
        #    raise RuntimeError('No arm selected!')

        forward = self.forward_box.value()
        turn = self.turn_box.value()

        if name == None:
            nname = self.name + str(self.counter)
        else:
            nname = name
        return TurtlebotMoveState(nname, forward, turn)
    
    def set_node_properties(self, gripper_state):
        if gripper_state.arm == 'left':
            self.radio_buttons[0].setChecked(True)
        if gripper_state.arm == 'right':
            self.radio_buttons[1].setChecked(True)

        self.gripper_box.set_value(gripper_state.gripper_size)
        self.effort_box.set_value(gripper_state.effort)

    def reset(self):
        self.gripper_box.set_value(0.0)
        self.effort_box.set_value(50.)
        self.radio_buttons[0].setChecked(True)


class TurtlebotMoveState(tu.SimpleStateBase): # smach_ros.SimpleActionState):

    def __init__(self, name, forward, turn):
        action = 'turtlebot_move'

        tu.SimpleStateBase.__init__(self, name, \
                action, pm.TurtlebotMoveAction,
                goal_cb_str = 'ros_goal')

        self.turn = turn
        self.forward = forward

    def ros_goal(self, userdata, default_goal):
        #import time
        #while True:
        #    time.sleep(.01)
        return pm.TurtlebotMoveGoal(self.turn, self.forward)

    def __getstate__(self):
        state = tu.SimpleStateBase.__getstate__(self)
        my_state = [self.forward, self.turn]
        return {'simple_state': state, 'self': my_state}

    def __setstate__(self, state):
        tu.SimpleStateBase.__setstate__(self, state['simple_state'])
        self.forward, self.turn = state['self']

