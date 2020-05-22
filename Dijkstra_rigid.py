# ENPM 661 PROJECT 2
# Varun Asthana, Jaad Lepak, Anshuman Singh

# =====SECTION 1: LIBRARIES=====
import numpy as np
import copy as cp
import math
import matplotlib.pyplot as plt
import cv2
import time

# =====SECTION 2: MAPS=====

# Final fixed map that has five obstacles
class FinalMap():
    def __init__(self, height, width, clr):
        """Initializes final map
        height:     row dimension [pixels]
        width:      column dimension [pixels]
        clr:        clearance from map border"""
        height+=1
        width+=1
        self.c = clr
        self.grid= np.ones([height,width,3], dtype ='uint8')*255
        # self.steps= ['T','L','R','B','TL', 'TR', 'BL', 'BR']
        self.grid[0:(clr+1),:,0] = 0
        self.grid[height-(clr+1):height,:,0] = 0
        self.grid[:,0:(clr+1),0] = 0
        self.grid[:, width-(clr+1):width,0] = 0

    # Obstacle in top left
    def shape1(self):
        """Fixed polygon shape for obstacle in top-left of map"""
        m1, c1 = 13.0, -140
        m2, c2 = 0, 185
        m3, c3 = 7.0/5, 80
        m4, c4 = 1, 100
        m5, c5 = -(7.0/5), 290
        m6, c6 = (6.0/5), 30
        m7, c7 = -(6.0/5), 210
        for x in range(self.grid.shape[1]/2):
            for y in range (self.grid.shape[0]):
                y1= m1*x + c1 + (self.c)*math.sqrt(1+(m1**2))
                y2= m2*x + c2 + (self.c)*math.sqrt(1+(m2**2))
                y3= m3*x + c3 - (self.c)*math.sqrt(1+(m3**2))
                y4= m4*x + c4 - (self.c)*math.sqrt(1+(m4**2))
                if(y<=y1 and y<=y2 and y>=y3 and y>=y4):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=0
                y3a= m3*x + c3 + (self.c)*math.sqrt(1+(m3**2))
                y5= m5*x + c5 + (self.c)*math.sqrt(1+(m5**2))
                y6= m6*x + c6 - (self.c)*math.sqrt(1+(m6**2))
                y7= m7*x + c7 - (self.c)*math.sqrt(1+(m7**2))
                if(y<=y3a and y<=y5 and y>=y6 and y>=y7):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=0

                if(y<=y2 and y>y5 and y>(self.c) and y<(self.grid.shape[0]-(self.c+1))):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=255

                if(y>y2 and y<y3a and y>(self.c) and y<(self.grid.shape[0]-(self.c+1))):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=255
        # Highlighting the vertices of the polygons
        self.grid[self.grid.shape[0]-1-120,75,0:2]= 0
        self.grid[self.grid.shape[0]-1-185,25,0:2]= 0
        self.grid[self.grid.shape[0]-1-185,75,0:2]= 0
        self.grid[self.grid.shape[0]-1-150,100,0:2]= 0
        self.grid[self.grid.shape[0]-1-150,50,0:2]= 0
        self.grid[self.grid.shape[0]-1-120,20,0:2]= 0
        return

    # Obstacle in center
    def ellipse(self, major, minor, h, w):
        """Customiazble ellipse obstacle
            major:  major axis dimension [pixels]
            minor:  minor axis dimension [pixels]
            h:      ellipse center location in map's coordinate system
            w:      ellipse center location in map's coordinate system"""
        finalMajor= major + self.c
        finalMinor= minor + self.c
        if(h- finalMinor <=0):
            ha= 0
        else:
            ha= h - finalMinor
        if(h+finalMinor >= self.grid.shape[0]):
            hb= self.grid.shape[0]
        else:
            hb= h + finalMinor

        if(w- finalMajor <=0):
            wa= 0
        else:
            wa= w-finalMajor

        if(w+finalMajor >= self.grid.shape[1]):
            wb= self.grid.shape[1]
        else:
            wb= w + finalMajor

        for i in range(wa, wb):
            for j in range(ha, hb):
                if ((float(i - w) / finalMajor) ** 2 + (float(j - h) / finalMinor) ** 2) <= 1:
                    self.grid[200-j, i, 0] = 0
        return

    # Obstacle in top right
    def circ(self, radius, h, w):
        """Customizable circle obstacle
            radius:     radius dimention [pixels]
            h:          circle center location in map's coordinate system
            w:          circle center location in map's coordinate system"""
        finalRad = radius + self.c
        if(h-finalRad<0):
            ha=0;
        else:
            ha= h - finalRad

        if(h+finalRad >= self.grid.shape[0]):
            hb= self.grid.shape[0]
        else:
            hb= h + finalRad

        if(w-finalRad<0):
            wa=0;
        else:
            wa= w - finalRad

        if(w+finalRad >= self.grid.shape[1]):
            wb= self.grid.shape[1]
        else:
            wb= w + finalRad

        for h_ in range(ha, hb):
            for w_ in range(wa, wb):
                eqn= (h_-h)**2 + (w_-w)**2
                if(eqn<=(finalRad**2)):
                    self.grid[h_,w_,0] = 0
        return

    # Obstacle in bottom right
    def rohmbus(self):
        """Fixed polygon shape for obstacle in bottom-right of map"""
        m1, c1 = -(3.0/5), 295
        m2, c2 = (3.0/5), 25
        m3, c3 = -(3.0/5), 325
        m4, c4 = (3.0/5), 55

        # for y in range(self.grid.shape[0]):
        for x in range(self.grid.shape[1]):
            for y in range (self.grid.shape[0]):
                y1= m1*x + c1 - (self.c)*math.sqrt(1+(m1**2))
                y2= m2*x + c2 - (self.c)*math.sqrt(1+(m2**2))
                y3= m3*x + c3 + (self.c)*math.sqrt(1+(m3**2))
                y4= m4*x + c4 + (self.c)*math.sqrt(1+(m4**2))
                if(y>=y1 and y>=y2 and y<=y3 and y<=y4):
                    self.grid[y,x, 0]=0
        # Highlighting the rohmbus vertices
        self.grid[175,200,0:2]= 0
        self.grid[160,225,0:2]= 0
        self.grid[175,250,0:2]= 0
        self.grid[190,225,0:2]= 0
        return

    # Obstacle in bottom left
    def rect(self):
        """Fixed polygon shape for obstacle in bottom-left of map"""
        m1, c1 = -(9.0/5), 186
        m2, c2 = (38.0/65), (1333.0/13)
        m3, c3 = -(9.0/5), 341
        m4, c4 = (38.0/65), (1488.0/13)
        for x in range(self.grid.shape[1]):
            for y in range (self.grid.shape[0]):
                y1= m1*x + c1 - (self.c)*math.sqrt(1+(m1**2))
                y2= m2*x + c2 - (self.c)*math.sqrt(1+(m2**2))
                y3= m3*x + c3 + (self.c)*math.sqrt(1+(m3**2))
                y4= m4*x + c4 + (self.c)*math.sqrt(1+(m4**2))
                if(y>=y1 and y>=y2 and y<=y3 and y<=y4):
                    self.grid[y,x, 0]=0
        # Highlighting the rectangle vertices
        self.grid[132,30,0:2]= 0
        self.grid[123,35,0:2]= 0
        self.grid[161,100,0:2]= 0
        self.grid[170,95,0:2]= 0
        return


# =====SECTION 3: ACTIONS AND NODES=====
def Action(move):
    """8-action move set for robot
        T moves up, costs 1
        L moves left, costs 1
        R moves right, costs 1
        B moves down, costs 1
        TL moves up-left, costs sqrt(2)
        TR moves up-right, costs sqrt(2)
        BL moves down-left, costs sqrt(2)
        BR moves down-right, costs sqrt(2)
        Returns new node position and cost value of the action"""
    actions= {'T': [np.array([-1,0]),1.0], 'L': [np.array([0,-1]),1.0],
              'R': [np.array([0,1]),1.0], 'B': [np.array([1,0]),1.0],
              'TL':[np.array([-1,-1]),math.sqrt(2)], 'TR': [np.array([-1,1]),math.sqrt(2)],
              'BL':[np.array([1,-1]),math.sqrt(2)], 'BR': [np.array([1,1]),math.sqrt(2)] }
    return actions[move]


class AllNodes():
    # Initialize class object
    def __init__(self, height, width):
        """Initializes to keep track of all nodes explored"""
        self.h_ = height + 1
        self.w_ = width + 1
        self.allStates=[]
        self.visited= np.zeros([self.h_, self.w_])
        self.ownIDarr= np.ones([self.h_, self.w_], dtype='int64')*(-1)
        self.pIDarr= np.ones([self.h_, self.w_], dtype='int64')*(-1)
        self.cost2come= np.ones([self.h_, self.w_], dtype='f')*(float('inf'))

    # Function to mark the node as visited in the visited array
    def updateVisited(self, cord):
        self.visited[cord[0], cord[1]] = 1
        return

    # Function to get update cost in cost2come array
    def updateCost(self, cord, cost, pid):
        if(self.cost2come[cord[0],cord[1]] > cost):
            self.cost2come[cord[0],cord[1]] = cost
            self.pIDarr[cord[0],cord[1]] = pid
        return

    # Function to add new unique node in the Nodes data set
    def push(self, cord):
    	self.ownIDarr[cord[0],cord[1]] = int(len(self.allStates))
    	# self.pIDarr[cord[0],cord[1]] = pid
        self.allStates.append(cord)

        return

    # Function to get own id
    def getOwnId(self,cord):
        return self.ownIDarr[cord[0], cord[1]]

    # Function to get parent id
    def getParentId(self,cord):
        return self.pIDarr[cord[0], cord[1]]

    # Function to get state of the node i.e. coordinate [h,w[]
    def getStates(self, idx):
        return self.allStates[idx]

    # Function to get the index value of cost2come array having minimum cost value
    def minCostIdx(self):
        try:
            newMin= np.min(self.cost2come[self.cost2come>0])
            index= np.argwhere(self.cost2come==newMin)[0]
            if(newMin == float('inf')):
                status= False
            else:
                status= True
        except:
            newMin = float ('inf')
            index = np.array([-1,-1])
            status= False
        return status, newMin, index

# =====SECTION 4: USER INPUT=====

# Set as point robot
checkInp= True
while checkInp:
    print('Enter the radius and clearance (enter 0,0 for point robot) [separated by commas]: ')
    print('Ceil value of radius + clearance will be considered')
    a = input()
    if(len(a)==2):
        rad= a[0]
        clr= a[1]
        checkInp= False
    else:
        print 'Wrong input....Try again'
tot= int(math.ceil(rad+clr))

# --- Use Final Map ---
map1= FinalMap(200, 300, tot)
map1.shape1()
map1.circ(25, 50, 225)
map1.ellipse(40, 20, 100, 150)
map1.rohmbus()
map1.rect()

# Save map as an jpg image
cv2.imwrite('grid_init.jpg',map1.grid)
map2= cv2.imread('grid_init.jpg')
map2 = cv2.cvtColor(map2, cv2.COLOR_BGR2RGB)
plt.ion()
plt.imshow(map2)
plt.show()

# Get starting position from user
graph= AllNodes(200,300) # graph object created for allNodes class
checkInp= True
while checkInp:
    print('Enter the initial starting coordinates with origin at bottom left as x,y in integer [separated by commas]: ')
    cart= np.array(input(), dtype='int')
    init= np.array([200-cart[1], cart[0]])
    if(len(cart)!=2 or init[0]<=0 or init[1]<=0 or init[0]>=map1.grid.shape[0]-1 or init[1]>=map1.grid.shape[1]-1):
        print 'Wrong input....Try again \nNote: Only 2 positive integers needed inside the map boundaries'
    else:
        if(map1.grid[init[0],init[1],0] == 0):
            print 'Start position cannot be from the obstacle node.....Try again'
        else:
            checkInp = False

# Get goal position from user
checkInp= True
while checkInp:
    print('Enter the goal coordinates with origin at bottom left as x,y in integer [separated by commas]: ')
    fs= np.array(input(), dtype='int')
    finalState= np.array([200-fs[1], fs[0]])
    if(len(fs)!=2 or finalState[0]<=0 or finalState[1]<=0 or finalState[0]>=map1.grid.shape[0]-1 or finalState[1]>=map1.grid.shape[1]-1):
        print 'Wrong input....Try again \nNote: Only 2 positive integers needed inside the map boundaries'
    else:
        if(map1.grid[finalState[0],finalState[1],0] == 0):
            print 'Goal position cannot be the obstacle node.....Try again'
        else:
            checkInp = False

plt.ioff()
parentState= init
parentCost= 0
parentId= 0
# appending the first node into allNodes data set
graph.push(parentState)
graph.pIDarr[parentState[0], parentState[1]]=0
graph.updateVisited(parentState)
graph.updateCost(parentState, parentCost, parentId)
found= False

# check if initial state is same as final state
compare= parentState == finalState
if(compare.all()):
    found =True
    print('Input position is same as goal position')

# =====SECTION 5: EXPLORATION=====
# Record time
start_time = time.time()
print('Processing...')
idx= 0
moves= ['T','L','R','B','TL', 'TR', 'BL', 'BR']
count = 0
plt.ion()
minCost= 0.0
idx=0
while(found != True):
    # current node is termed as parent node    
    for act in moves: # Iterating for all possible 8 actions
        step = Action(act)
        tempState = parentState + step[0]
        if(map1.grid[tempState[0],tempState[1],0]!=0 and graph.visited[tempState[0],tempState[1]]==0):
            tempCost = parentCost + step[1]
            graph.updateCost(tempState, tempCost, parentId)
    
    status, minCost, parentState = graph.minCostIdx()
    if(not status):
        print('No solution exist, terminating....')
        count=1
        break
    map1.grid[parentState[0], parentState[1],1]=40
    map1.grid[parentState[0], parentState[1],0]=0
    parentCost = graph.cost2come[parentState[0], parentState[1]]
    graph.updateCost(parentState, parentCost, parentId)
    graph.cost2come[parentState[0], parentState[1]]= graph.cost2come[parentState[0], parentState[1]]*(-1)
    graph.push(parentState)
    graph.updateVisited(parentState)
    parentId = graph.getOwnId(parentState)
    compare= parentState == finalState
    if(compare.all()):
        found =True
        print('Solved')
        break

# Write explored area to map image
cv2.imwrite('gridExplored.jpg',map1.grid)

# =====SECTION 6: PATH GENERATION=====
# Print final time
print("Time explored = %2.3f seconds " % (time.time() - start_time))

# back-tracking for the shortest path and appending the path in result
ans= graph.getOwnId(finalState)
map2= cv2.imread('gridExplored.jpg')
map2 = cv2.cvtColor(map2, cv2.COLOR_BGR2RGB)

if(not count):
	print '\nYellow area shows all the obstacles and White area is the free space'
	print 'Red area shows all the explored Nodes (area)'
	print 'Blue line shows optimal path (traced from goal node to start node)'
# Draw path
while(ans!=0 and count==0):
    plt.cla()
    startNode= graph.getStates(ans)
    ans= graph.getParentId(startNode)
    nextNode= graph.getStates(ans)
    cv2.line(map2, (startNode[1],startNode[0]),(nextNode[1],nextNode[0]),(0,0,255),1)
    plt.imshow(map2)
    plt.show()
    plt.pause(0.000001)

plt.cla()
plt.imshow(map2)
# User exit
print('Enter any NUMBER to exit: ')
input()
map2 = cv2.cvtColor(map2, cv2.COLOR_RGB2BGR)
cv2.imwrite('back_tracking.jpg',map2)
plt.ioff()