#Takes a training list txt file as an input. Returns two lists, one with the rewarded pixels and one which indicates which pixels to play.

import numpy as np

def trajectoryInput():
    day = input("What day of training is this?")
    
    filename = 'traininglist_' + str(day) + '.txt' # Determine the filename for the traininglist trajectory
    
    with open (filename, 'r') as f:
        training_list = f.readlines()
        #training_list = [x.strip() for x in training_list] 
        #This opens the trajectory list file for that day and turns it into a list
    
    #Find the Rewarded Pixels based on the pixels that fall between % in our training list.
    rewardIndices = []
    for i, elem in enumerate(training_list):
        if '%' in elem:
            rewardIndices.append(i)
    rew = training_list[((rewardIndices[0])+1):rewardIndices[1]]
    rew = list(map(int,rew))
    
    #Separates trajectory list from reward list and turns it into pos. pos is a list of integers indicating which pixels to play
    pos = training_list[((rewardIndices[1])+1):-1]
    pos = list(map(int,pos))
    
    return (rew, pos)
