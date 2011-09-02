#Melonee Wise <mwise@willowgarage.com>
import roslib; 
roslib.load_manifest('turtlebot_rcommander_tools')
import rcommander.tool_utils as tu
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import rosgraph.masterapi
import string
import functools as ft
import turtlebot_actions.msg as ta


class RemapperTool(tu.ToolBase):
  def __init__(self, rcommander):
    tu.ToolBase.__init__(self, rcommander, 
                         'remapper', 
                         'Action Msg Remapper', 
                         ActionMsgMapperState)

  def fill_property_box(self, pbox):
    formlayout = pbox.layout()
    self.topics = rosgraph.masterapi.Master('/rostopic').getTopicTypes()
    self.input_topics = QComboBox(pbox)
    self.output_topics = QComboBox(pbox)
    for topic in self.topics:
      self.input_topics.addItem(topic[0])
      self.output_topics.addItem(topic[0])

    formlayout.addRow("&Input Topic", self.input_topics)
    formlayout.addRow("&Output Topic", self.output_topics)

    self.input_list = QLineEdit(pbox)
    formlayout.addRow('&Input Remap List', self.input_list)
    self.output_list = QLineEdit(pbox)
    formlayout.addRow('&Output Remap List', self.output_list)

    pbox.update()


  def new_node(self, name=None):
    input_topic = self.topics[self.input_topics.currentIndex()][0]
    print input_topic
    output_topic = self.topics[self.output_topics.currentIndex()][0]
    input_type = self.topics[self.input_topics.currentIndex()][1]
    output_type = self.topics[self.output_topics.currentIndex()][1]
    print output_type
    
    if name == None:
      nname = self.name + str(self.counter)
    else:
      nname = name
    return ActionMsgMapperState(nname, 
                                input_topic,
                                output_topic,
                                input_type,
                                output_type,
                                str(self.input_list.text()),
                                str(self.output_list.text()))

  def set_node_properties(self, node):
    self.input_topics.setCurrentIndex(self.input_topics.findText(node.input_topic))
    self.output_topics.setCurrentIndex(self.output_topics.findText(node.output_topic))

    self.input_list.setText(string.join(node.input_list, ', '))
    self.output_list.setText(string.join(node.output_list, ', '))

  def reset(self):
    self.input_topics.setCurrentIndex(0)
    self.output_topics.setCurrentIndex(0)
    self.input_list.setText('')
    self.output_list.setText('')

class ActionMsgMapperState(tu.SimpleStateBase): 
  def __init__(self, name, input_topic, output_topic, input_type, output_type, input_list, output_list):
    tu.SimpleStateBase.__init__(self, name,
                                'remapper', 
                                ta.ActionMsgMapperAction,
                                goal_cb_str = 'ros_goal')


    self.input_topic = input_topic
    self.output_topic = output_topic
    self.input_type = input_type
    self.output_type = output_type

    self.input_list = [item.strip() for item in  input_list.split(',')]
    self.output_list = [item.strip() for item in output_list.split(',')]


  def ros_goal(self, userdata, default_goal):
    goal = ta.ActionMsgMapperGoal()
    goal.input_topic = self.input_topic
    goal.output_topic = self.output_topic
    goal.input_type = self.input_type
    goal.output_type = self.output_type
    goal.input_list = self.input_list
    goal.output_list = self.output_list

    return goal

  def __getstate__(self):
    state = tu.SimpleStateBase.__getstate__(self)
    my_state = [self.input_topic, self.output_topic, 
                self.input_type, self.output_type, 
                self.input_list, self.output_list]
    return {'simple_state': state, 'self': my_state}
  
  def __setstate__(self, state):
    tu.SimpleStateBase.__setstate__(self, state['simple_state'])
    self.input_topic, self.output_topic, self.input_type, self.output_type, self.input_list, self.output_list = state['self']
