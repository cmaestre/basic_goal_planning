# -*- coding: utf-8 -*-
"""
Created on Thu May 18 15:56:51 2017

@author: maestre
"""

from __future__ import print_function

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches
import copy
import rospy
import time

from basic_goal_planning.srv import *
from baxter_kinematics.srv import *

''' Find path from env 0 to env goal '''
def find_path(transitions_vector,
              env_goal):
    
    path = []
    action_vector = []
    if env_goal == 0:
        print('Already on initial state')
    else:
        tmp_goal = copy.copy(env_goal)
        path.append(tmp_goal)
        path_found = False
        rev_transitions_vector = copy.copy(transitions_vector)
        rev_transitions_vector.reverse()
        while not path_found:
            prev_state = -1
            for curr_trans in rev_transitions_vector:
                if curr_trans[2] == tmp_goal:
                    prev_state = curr_trans[0]
                    break
            print(curr_trans[0], '>>', tmp_goal)
            action_vector.append(curr_trans[1])
            if prev_state == 0:
                path.append(prev_state)
                path_found = True
            else:                
                tmp_goal = curr_trans[0]
                path.append(tmp_goal)
    
    path.reverse()
    action_vector.reverse()
    return path, action_vector

def compute_transition_vector_python(transitions_vector):
    lines = open('dataset.txt', 'r').readlines()
    for line in lines:
        values_vector = line.split(' ')
        curr_transition = []
        curr_transition.append(int(values_vector[0]))
        curr_transition.append([round(float(values_vector[1]),3),
                                round(float(values_vector[2]),3)])
        curr_transition.append(int(values_vector[3]))
        transitions_vector.append(curr_transition)
    return transitions_vector

def plot_python(action_vector):
    fig = plt.figure(num=None, figsize=(8, 6), facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111, aspect='equal')
    p1 = plt.Rectangle((0.1, 0.4),0.2, 0.2, fc='b', zorder=0)
    p2 = plt.Rectangle((0.4, 0.4),0.2, 0.2, fc='b', zorder=0)
    p3 = plt.Rectangle((0.7, 0.4),0.2, 0.2, fc='b', zorder=0)
    plt.axis('off')
    ax.add_patch(p1)    
    ax.add_patch(p2)
    ax.add_patch(p3)

    c1 = plt.Circle((action_vector[0][1],
                     action_vector[0][0]), 
                     0.02, fc = 'green', zorder=10)
    ax.add_patch(c1)
    c2 = plt.Circle((action_vector[1][1],
                     action_vector[1][0]), 
                     0.02, fc = 'orange', zorder=10)
    ax.add_patch(c2)
    c3 = plt.Circle((action_vector[2][1],
                     action_vector[2][0]), 
                     0.02, fc = 'magenta', zorder=10)
    ax.add_patch(c3)    

def main(goal_state): 
               
    env_state = {0:'lever_off',
                 1:'lever_on',
                 2:'red_pushed',
                 3:'green_pushed'}
    
    ''' Compute planning '''    
    ## prev_state, action, next_state
    real_robot = True
    if real_robot:
        transitions_vector_predef = [(0, 0, 1),
                                     (1, 1, 0),
                                     (1, 2, 2),
                                     (2, 1, 0),
                                     (2, 3, 3),
                                     (3, 1, 0)]
        path, action_vector = find_path(transitions_vector_predef, goal_state)
        print('path_found')

        ''' Reset robot '''
        rospy.wait_for_service('baxter_kinematics/restart_robot')
        try:
            reset_robot = rospy.ServiceProxy('baxter_kinematics/restart_robot', RestartRobot)
            resp1 = reset_robot()
    #            return resp1.sum
        except rospy.ServiceException, e:
            print ("Service call failed: %s"%e)
            return 0    
        
        ''' Reset environment '''
    
        ''' Execute planning '''
        for traj_id in action_vector:
            rospy.wait_for_service('planning/exec_predef_traj')
            try:
                run_traj = rospy.ServiceProxy('planning/exec_predef_traj', ExecPredefTraj)
                resp1 = run_traj(traj_id)
            except rospy.ServiceException, e:
                print ("Service call failed: %s"%e)
                return 0
#        return 1        
        
    else:
        transitions_vector_python = []
        transitions_vector_python = compute_transition_vector_python(transitions_vector_python)   
        path, action_vector = find_path(transitions_vector_python, goal_state)
        plot_python(action_vector)
    
    print(path)
    print(action_vector)
        
    ''' Turn everything off '''
#    time.sleep(3)    
    rospy.wait_for_service('planning/exec_predef_traj')
    try:
        run_traj = rospy.ServiceProxy('planning/exec_predef_traj', ExecPredefTraj)
        resp1 = run_traj(1)
    except rospy.ServiceException, e:
        print ("Service call failed: %s"%e)
        return 0

    return 1


if __name__ == '__main__':
    goal_state = 3    
    main(goal_state)
    
    
    
    
    