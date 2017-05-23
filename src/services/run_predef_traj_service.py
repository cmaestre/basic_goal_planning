#!/usr/bin/env python

from __future__ import print_function

from basic_goal_planning.srv import *
from baxter_kinematics.srv import *
import rospy

def execute_predef_traj(req):
    
    ## connect to execute traj service
    rospy.wait_for_service('/baxter_kinematics/execute_trajectory')
    
    ## predefined actions
#    actions = {0:[[0.3, 0.6, 0.1],
#                  [0.3, 0.6, -0.15], 
#                  [0.5, 0.6, -0.1],
#                  [0.5, 0.6, 0.1]], ##'l_on',
#               1:[[0.65, 0.6, 0.1], 
#                  [0.65, 0.6, -0.15], 
#                  [0.5, 0.6, -0.1],
#                  [0.5, 0.6, 0.1]], ##'l_off',
#               2:[[0.5, 0.3, 0.3], 
#                  [0.5, 0.3, -0.15],
#                  [0.5, 0.3, 0]], ##'push_red_button',
#               3:[[0.5, 0, 0.3], 
#                  [0.5, 0, -0.15],
#                  [0.5, 0, 0]]} ##'push_green_button'}    

    actions = {0:[[0.6, 0.28, 0.1],
                  [0.6, 0.28, -0.13], 
#                  [0.8, 0.28, -0.1],
                  [0.8, 0.28, 0]], ##'l_on',
                  
               1:[[0.8, 0.28, 0.1], 
                  [0.75, 0.28, -0.13], 
#                  [0.5, 0.6, -0.1],
                  [0.5, 0.28, 0.1]], ##'l_off',
                  
               2:[[0.68, 0.1, 0.1], 
                  [0.68, 0.1, -0.1],
                  [0.68, 0.1, 0]], ##'push_red_button',
                  
               3:[[0.7, -0.075, 0.1], 
                  [0.7, -0.075, -0.1],
                  [0.7, -0.075, 0]]} ##'push_green_button'}    
    
    try:
        move_pos = rospy.ServiceProxy('/baxter_kinematics/move_to_position', MoveToPos)
        ## right arm
        resp1 = move_pos('right',
                          0.25, -0.5, 0.4)
        
        ## left arm
        exec_traj = rospy.ServiceProxy('/baxter_kinematics/execute_trajectory', Trajectory)
        curr_traj_id = req.id_traj
        if curr_traj_id >= 0 and curr_traj_id <= 3:
            tmp = actions[curr_traj_id]
            curr_traj = [v for x in tmp for v in x]
        else:
            print('ERROR - execute_predef_traj : unknown traj ID', curr_traj_id)
            return False
        
        resp1 = exec_traj('left', 
                          curr_traj,
                          False)
        return resp1.success
    except rospy.ServiceException, e:
        print ("Service call to execute_trajectory failed: %s"%e)
    

def execute_predef_traj_service():
    rospy.init_node('execute_predef_traj_service')
    rospy.Service('planning/exec_predef_traj', ExecPredefTraj, execute_predef_traj)
    print ("Ready to execute a predefined trajectory")
    rospy.spin()

if __name__ == "__main__":
    execute_predef_traj_service()