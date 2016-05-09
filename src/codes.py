import numpy as np

#Codes definitions
codes=  [

[[ 0,  0,  0,  0,  0,  0,  0],
 [ 0,  1,  0,  0,  1,  1,  0],
 [ 0,  0,  1,  1,  0,  0,  0],
 [ 0,  0,  1,  0,  0,  1,  0],
 [ 0,  0,  1,  0,  0,  1,  0],
 [ 0,  0,  0,  1,  0,  1,  0],
 [ 0,  0,  0,  0,  0,  0,  0]],

[[ 0,  0,  0,  0,  0,  0,  0,],
 [ 0,  1,  1,  1,  0,  1,  0,],
 [ 0,  0,  0,  0,  1,  0,  0,],
 [ 0,  1,  0,  1,  1,  1,  0,],
 [ 0,  1,  0,  1,  1,  1,  0,],
 [ 0,  1,  0,  1,  0,  1,  0,],
 [ 0,  0,  0,  0,  0,  0,  0,]],

[[ 0,  0,  0,  0,  0,  0,  0,],
 [ 0,  0,  1,  1,  0,  1,  0,],
 [ 0,  1,  0,  0,  1,  0,  0,],
 [ 0,  0,  1,  1,  1,  0,  0,],
 [ 0,  0,  1,  1,  1,  0,  0,],
 [ 0,  1,  1,  1,  0,  0,  0,],
 [ 0,  0,  0,  0,  0,  0,  0,]],

[[ 0,  0,  0,  0,  0,  0,  0,],
 [ 0,  0,  1,  0,  0,  1,  0,],
 [ 0,  1,  0,  1,  1,  0,  0,],
 [ 0,  1,  1,  0,  0,  0,  0,],
 [ 0,  1,  1,  0,  0,  0,  0,],
 [ 0,  0,  1,  1,  1,  0,  0,],
 [ 0,  0,  0,  0,  0,  0,  0,]],

]

#Helper functions
def validCode(c):
    '''Make sure code is valid, ie, can be uniquely identified in any orientation'''
    for i in range(1,4):
        rot = np.rot90(c,i)
        if np.array_equal(c, rot):
            return False

    return True

def matchCode(cp):
    '''Given a code pattern, return the code ID and orientation'''

    id = -1
    orie = 0

    differences = [np.sum(cp != c) for c in codes]
    idx = np.argmin(differences)

    #If has less than 5 different cells considers a match
    if differences[idx] < 5:
        id = np.floor_divide(idx, 4)
        orie = np.mod(idx, 4)

    return id, orie

#Get only valid codes
codes = [np.array(c) for c in codes]
codes = [c for c in codes if validCode(c)]
n = len(codes)
cells = codes[0].shape[0]

#Generate extended code list, with all possible orientations
codesExt = []
for c in codes:
    for i in (0,3,2,1):
        codesExt.append(np.rot90(c, i))
codes = codesExt
