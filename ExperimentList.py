#This script creates a txt file containing which lists to use from which folders


filename = 'ExperimentLists.txt'
f = open(filename,'w')
f.write('#EXPERIMENT LISTS\n')

#RW: Random Walk
#Traj: Trajectory
#RJ: Random Jump

#This list keeps track of which list type to use
ListType = ['RW+Traj', 'RW+RJ', 'RW','RW+Traj','RW+RJ', 'RW','RW+Traj']

#This list tracks how many sessions to take for the above List Types
ListNumber = [24, 3, 10, 6, 3, 10, 6]

#This list keeps track of what set of rewards the animal is on
Reward_Set = [1,1,2,2,2,3,3]


#This keeps track of which number the list is currently on
ListTrack = [0, 0, 0, 0, 0]
ListTrackTypes = ['RW', 'Traj', 'RJ', 'RW+Traj', 'RW+RJ']

s = 0
#first loop through each element in ListType - the tuple containing the sequence of lists to use
#in the experiment
for i,Type in enumerate(ListType):
    #loop through each type of list in order to determine which is the current list. Once this
    #is determined, the current element within the list is determined
    for j,types in enumerate(ListTrackTypes):
        if Type == types:
            curr = j
            break
    #now loop through each 'session' in the current ListType and create a new line in the text
    #file with the relecant information for the session
        
    #'s' keeps track of the current session
    for sess in range(ListNumber[i]):
        s = s + 1
        ListTrack[j] += 1
        f.write(str(s) + ',' + str(ListTrack[j]) + ',' + Type + ',' + str(Reward_Set[i]) +  '\n')

f.close()
        
