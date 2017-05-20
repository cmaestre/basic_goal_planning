# -*- coding: utf-8 -*-
"""
Created on Thu May 18 15:56:51 2017

@author: maestre
"""

#from __future__ import print_function

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches
import copy

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

    print('path_found')
    path.reverse()
    action_vector.reverse()
    return path, action_vector

def plot_scenario():
    fig = plt.figure(num=None, figsize=(8, 6), facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111, aspect='equal')
    p1 = plt.Rectangle((0.1, 0.4),0.2, 0.2, fc='b', zorder=0)
    p2 = plt.Rectangle((0.4, 0.4),0.2, 0.2, fc='b', zorder=0)
    p3 = plt.Rectangle((0.7, 0.4),0.2, 0.2, fc='b', zorder=0)
#    pointer = plt.Circle((0.5,0.1), 0.02, fc = 'k', zorder=10)
    plt.axis('off')
#    return pointer
    ax.add_patch(p1)    
    ax.add_patch(p2)
    ax.add_patch(p3)
    
    return ax
    

def main(): 

    actions = {'a1':'l_far',
               'a2':'l_close',
               'a3':'push_red_button',
               'a4':'push_green_button'}
               
    env_state = {0:'lever_off',
                 1:'lever_on',
                 2:'red_pushed',
                 3:'green_pushed'}
    
    ## prev_state, action, next_state
#    transitions_vector = [(0, 'a1', 1),
#                        (1, 'a2', 0),
#                        (1, 'a3', 2),
#                        (2, 'a2', 0),
#                        (2, 'a4', 3)]
    
    transitions_vector = []
    lines = open('dataset.txt', 'r').readlines()
    for line in lines:
        values_vector = line.split(' ')
        curr_transition = []
        curr_transition.append(int(values_vector[0]))
        curr_transition.append([round(float(values_vector[1]),3),
                                round(float(values_vector[2]),3)])
        curr_transition.append(int(values_vector[3]))
        transitions_vector.append(curr_transition)
    path, action_vector = find_path(transitions_vector, 3)
    print(path)
    print(action_vector)
    
    ax = plot_scenario()
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
    
#    for traj_id in path:
#        rospy.wait_for_service('run_predef_traj')
#        try:
#            run_traj = rospy.ServiceProxy('run_predef_traj', RunPredefTraj)
#            resp1 = run_traj(id_traj)
#            return resp1.sum
#        except rospy.ServiceException, e:
#            print "Service call failed: %s"%e                 


if __name__ == '__main__':
    main()
    
    
    
    
    