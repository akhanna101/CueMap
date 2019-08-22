#This script creates a txt file containing which lists to use from which folders


filename = 'ExperimentLists.txt'
f = open(filename,'w')
f.write('#EXPERIMENT LISTS\n')

#RW: Random Walk
#Traj: Trajectory
#RJ: Random Jump

#This list keeps track of which list type to use
ListType = ['RW+Traj', 'RW+RJ', 'RW','RW+Traj']

#This list tracks how many sessions to take for the above List Types
ListNumber = [24, 3, 6,10]

#This keeps track of which number the list is currently on
ListTrack = [0, 0, 0, 0, 0]
ListTrackTypes = ['RW', 'Traj', 'RJ', 'RW+Traj', 'RW+RJ']

s = 0    
for i,Type in enumerate(ListType):
    for j,types in enumerate(ListTrackTypes):
        if Type == types:
            curr = j
            break
    for sess in range(ListNumber[i]):
        s = s + 1
        ListTrack[j] += 1
        f.write(str(s) + ',' + str(ListTrack[j]) + ',' + Type + '\n')

f.close()
        
