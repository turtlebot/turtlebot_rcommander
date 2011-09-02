#Melonee Wise <mwise@willowgarage.com>
import roslib; 
roslib.load_manifest('turtlebot_rcommander_tools')
import rcommander.tool_utils as tu
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time

import functools as ft
import turtlebot_actions.msg as ta


class FindFiducialTool(tu.ToolBase):
  def __init__(self, rcommander):
    tu.ToolBase.__init__(self, rcommander, 
                         'find_fiducial', 
                         'Find Fiducial Pose', 
                         FindFiducialState)

  def fill_property_box(self, pbox):
    self.patterns = {0:"CHESSBOARD",
                     1:"CIRCLES_GRID",
                     2:"ASYMMETRIC_CIRCLES_GRID"}
    formlayout = pbox.layout()
    self.camera = QLineEdit(pbox)
    formlayout.addRow('&Camera', self.camera)
    self.width =  QLineEdit(pbox)
    self.width.setText('0')
    formlayout.addRow('&Width', self.width)
    self.height =  QLineEdit(pbox)
    self.height.setText('0')
    formlayout.addRow('&Height', self.height)
    self.size =  QLineEdit(pbox)
    self.size.setText('0')
    formlayout.addRow('&Size', self.size)
    self.pattern_type = QComboBox(pbox)
    self.pattern_type.addItem(self.patterns[0])
    self.pattern_type.addItem(self.patterns[1])
    self.pattern_type.addItem(self.patterns[2])

    formlayout.addRow("&Pattern Type", self.pattern_type)
    pbox.update()


  def new_node(self, name=None):
    pattern_type = self.pattern_type.currentIndex()
    if name == None:
      nname = self.name + str(self.counter)
    else:
      nname = name
    return FindFiducialState(nname, 
                             str(self.camera.text()),
                             int(self.width.text()),
                             int(self.height.text()),
                             float(self.size.text()),
                             pattern_type)

  def set_node_properties(self, node):
    self.camera.setText(node.camera)
    self.width.setText(str(node.width))
    self.height.setText(str(node.height))
    self.size.setText(str(node.size))
    self.pattern_type.setCurrentIndex(node.pattern_type)

  def reset(self):
    self.camera.setText('')
    self.width.setText('0')
    self.height.setText('0')
    self.size.setText('0')
    self.pattern_type.setCurrentIndex(0)

class FindFiducialState(tu.SimpleStateBase): 
  def __init__(self, name, camera, width, height, size, pattern_type):
    tu.SimpleStateBase.__init__(self, name,
                                'find_fiducial_pose', 
                                ta.FindFiducialAction,
                                goal_cb_str = 'ros_goal')
    self.camera = camera
    self.width  = width
    self.height = height
    self.size   = size
    self.pattern_type = pattern_type


  def ros_goal(self, userdata, default_goal):
    goal = ta.FindFiducialGoal()
    goal.camera_name    = self.camera
    goal.pattern_width  = self.width
    goal.pattern_height = self.height
    goal.pattern_size   = self.size
    goal.pattern_type   = self.pattern_type
    print 'GOAL',goal.camera_name, goal.pattern_width, goal.pattern_height, goal.pattern_size, goal.pattern_type
    return goal

  def __getstate__(self):
    state = tu.SimpleStateBase.__getstate__(self)
    my_state = [self.name, self.camera, 
                self.width, self.height, 
                self.size, self.pattern_type]
    return {'simple_state': state, 'self': my_state}
  
  def __setstate__(self, state):
    tu.SimpleStateBase.__setstate__(self, state['simple_state'])
    self.name, self.camera, self.width, self.height, self.size, self.pattern_type = state['self']
