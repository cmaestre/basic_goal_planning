#from __future__ import print_function

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches
import copy
import rospy

from crustcrawler_package.srv import *

''' Find path from env 0 to env goal '''
def find_path(transitions_vector,
              env_goal):
    
    path = []
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
            if prev_state == 0:
                path.append(prev_state)
                path_found = True
            else:                
                tmp_goal = curr_trans[0]
                path.append(tmp_goal)

    print('path_found')
    path.reverse()
    return path

def main(): 
    
#    rospy.init_node('run_planning_node')
#    rospy.spin()

    actions = {'a1':'l_far',
               'a2':'l_close',
               'a3':'push_red_button',
               'a4':'push_green_button'}
               
    env_state = {0:'lever_off',
                 1:'lever_on',
                 2:'red_pushed',
                 3:'green_pushed'}
    
    ## prev_state, action, next_state
    transitions_vector = [(0, 'a1', 1),
                        (1, 'a2', 0),
                        (1, 'a3', 2),
                        (2, 'a2', 0),
                        (2, 'a4', 3)]
                    
    path = find_path(transitions_vector,
                     3)
    for traj_id in path:
        rospy.wait_for_service('run_predef_traj')
        try:
            run_traj = rospy.ServiceProxy('run_predef_traj', RunPredefTraj)
            resp1 = run_traj(id_traj)
            return resp1.sum
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e                 
    

if __name__ == '__main__':
    main()
 
#def update(*args):      
#    global cell_matrix
#    cell_matrix = iterate(cell_matrix)
#    im.set_array(cell_matrix)
#    return im
#
#''' To show the matrix '''                    
#
#fig = plt.figure(num=None, figsize=(8, 6), facecolor='w', edgecolor='k')
#ax1 = fig1.add_subplot(111, aspect='equal')
#p1 = patches.Rectangle(
#        (0.1, 0.1),   # (x,y)
#        0.5,          # width
#        0.5,          # height
#    )
#p1 = patches.Rectangle(
#    (0.1, 0.4),   # (x,y)
#    0.2,          # width
#    0.2,          # heigh
#)
#p2 = patches.Rectangle(
#    (0.4, 0.4),   # (x,y)
#    0.2,          # width
#    0.2,          # heigh
#)
#p3 = patches.Rectangle(
#    (0.7, 0.4),   # (x,y)
#    0.2,          # width
#    0.2,          # heigh
#)
#ax1.add_patch(p1)
#ax1.add_patch(p2)
#ax1.add_patch(p3)
#
#p1.set_facecolor('red')
#
#plt.show()
##plt.axis('off')
#
#''' Run the animation ''' 
#ani = animation.FuncAnimation(fig, update, interval=500,
#                              frames=range(200),repeat=False)
#
#''' Record the animation '''  
#Writer = animation.writers['avconv']
#writer_ = Writer(fps=15, bitrate=1800)
#ani.save('jeu_vie.mp4', writer = writer_)
#
#''' Print the animation in a window'''  
#plt.show()
