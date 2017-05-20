import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches

import pickle
import sys
import time

''' To show the matrix '''                    

fig = plt.figure(num=None, figsize=(8, 6), facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111, aspect='equal')
p1 = plt.Rectangle((0.1, 0.4),0.2, 0.2, fc='b', zorder=0)
p2 = plt.Rectangle((0.4, 0.4),0.2, 0.2, fc='b', zorder=0)
p3 = plt.Rectangle((0.7, 0.4),0.2, 0.2, fc='b', zorder=0)
pointer = plt.Circle((0.5,0.1), 0.02, fc = 'k', zorder=10)
plt.axis('off')

status = np.asarray(np.zeros(3))
statusBank = []
trajBank = []
NumOfEffectsFound = 0

def init():
    ax1.add_patch(p1)    
    ax1.add_patch(p2)
    ax1.add_patch(p3)
    pointer.center = (0.5,0.1)
    ax1.add_patch(pointer)
    return p1, p2, p3, pointer

def babbling(epicNum):
    traj =np.random.rand(1,2)
    return traj
    
def systemStatus(traj, status):
# UPDATES THE SYSTEM:
# Takes trajectory and the current status of the system, returns new status
        status1 = status
        if traj[0,0] > 0.4 and traj[0,0]<0.6:
            if traj[0,1] > 0.1 and traj[0,1] < 0.3: # BUTTON 1
                if status[0] == 1:
                    status1 = np.asarray([0,0,0]); #print('Status changed', status1)
                else:
                    status1 = [1,0,0]; #print('Status changed', status1)
            if traj[0,1] > 0.4 and traj[0,1] <0.6: # BUTTON 2
                if status[0] == 1 and status[1] == 0:
                    status1 = np.asarray([1,1,0]); #print('Status changed', status1)
                elif status[0] == 1 and status[1] == 1:
                    status1 = np.asarray([1,0,0]); #print('Status changed', status1)
                else:
                    status1 = status
            if traj[0,1] > 0.7 and traj[0,1] < 0.9: # BUTTON 3
                if status[0] == 1 and status[1] == 1:
                    status1 = np.asarray([1,1,1]); print('BUTTON 3!')
                elif all(status == [1,1,1]):
                    print('Error: should have terminated the episode in the last go, as [1,1,1] was reached')
                else:
                    status1 = status         
        else:
            status1 = status

        return status1 #(0,0,0)

def addToBank(status, status1, traj, trajBank, statusBank):
# FILLS TRAJECTORY BANK with the trajectories that led the the effect taking place (status being learned)
    if any(status1 != status):    
        trajBank.append(traj)
        statusBank.append(np.concatenate((status, status1), axis=0))
    return trajBank, statusBank
    
def update(*args): 
    
    # First Babbling:
    newTrajectory = babbling(1) # for one step (could probably extend it to a string later)
#    time.sleep(0.25)
    newStatus = np.asarray(systemStatus(newTrajectory, status))
    pointer.center = (newTrajectory[0,0], newTrajectory[0,1])

    # Effect detection
    if any(newStatus != status):
        global status
        global NumOfEffectsFound
        addToBank(status, newStatus, newTrajectory, trajBank, statusBank)
        print('Changes in status detected: ', newStatus)
        status = newStatus
        if status[0] == 1:
            p1.set_facecolor('red')
        elif status[0] == 0:
            p1.set_facecolor('blue')
        if status[1] == 1:
            p2.set_facecolor('red')
        elif status[1] == 0:
            p2.set_facecolor('blue')
        if status[2] == 1:
            p3.set_facecolor('red')
        elif status[2] == 0:
            p3.set_facecolor('blue')

    if np.shape(statusBank)[0] != 0:
        NumOfEffectsFound = np.shape(np.vstack({tuple(row) for row in np.asarray(statusBank)[:,3:6]}))[0]
    
    # Validation
    if NumOfEffectsFound >= 4 or all(newStatus == [1,1,1]):
        print('All effects learned. Stop the experiment.')
        f = open('ButtonEffects_DataBanks.pckl', 'wb')
        pickle.dump([statusBank, trajBank], f)
        f.close()
        plt.pause(30)   
    return p1, p2, p3, pointer

## Animation
''' Run the animation ''' 
ani = animation.FuncAnimation(fig, update, init_func=init,
                              interval=10,
                              frames=5,
                              repeat=True, blit=False)
    
#''' Record the animation '''  
#Writer = animation.writers['avconv']
#writer_ = Writer(fps=15, bitrate=1800)
#ani.save('jeu_vie.mp4', writer = writer_)
    
#''' Print the animation in a window'''  
plt.show()

print(len(trajBank))
print(len(statusBank))

def get_state_name(curr_state):
    if curr_state == [0, 0, 0]:
        return 0
    elif curr_state == [1, 0, 0]:
        return 1
    elif curr_state == [1, 1, 0]:
        return 2
    elif curr_state == [1, 1, 1]:
        return 3
    else:
        print('Wrong state', curr_state)
        return 4

with open('dataset.txt', 'w') as file:

    for pos in range(len(trajBank)):
        tmp = statusBank[pos][0:3].tolist()
        print(tmp)
#        for v in tmp:
#            file.write(str(int(v)))
#            file.write(' ')
        file.write(str(get_state_name(tmp)))
        file.write(' ')
            
        tmp = trajBank[pos][0].tolist()
        print(tmp)
        for v in tmp:
            file.write(str(float(v)))
            file.write(' ')            

        tmp2 = statusBank[pos][3:].tolist()
        print(tmp2)
#        for v in tmp:
#            file.write(str(int(v)))
#            file.write(' ')
        file.write(str(get_state_name(tmp2)))

        file.write('\n')
        print('\n')
    
    
    
    
