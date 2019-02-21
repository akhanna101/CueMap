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
    Rew = training_list[((rewardIndices[0])+1):rewardIndices[1]]
    Rew = list(map(int,Rew))
    
    #Separates trajectory list from reward list and turns it into list_path. list_path is a list of integers indicating which pixels to play
    list_path = training_list[((rewardIndices[1])+1):-1]
    list_path = list(map(int,list_path))
    
    return (Rew, list_path)