# Dijkstra Path Planner for point and rigid robot

## Overview

This project has two python scripts that generates a 2D map with obstacles and finds a path to travel from a user-defined start and end point.
<p align="center">
	<img src="https://github.com/varunasthana92/Dijkstra_Path_Planner/blob/master/sample_outputs/vid_point.gif" width="600">
	<br>
	Point Robot
</p>

<p align="center">
	<img src="https://github.com/varunasthana92/Dijkstra_Path_Planner/blob/master/sample_outputs/vid_rigid.gif" width="600"><br>
	Rigid Robot with effective clearance of 6 units
</p>

 __BOTH SCRIPTS REQUIRE PYTHON2.7 TO RUN. PYTHON3 WILL NOT WORK.__ Python 2.7 was used to test the scripts. One script is used for a point robot and the other is used for a rigid robot that has a defined radius and clearance. The code is organized in the following sections:

1. Libraries
2. Maps
3. Actions and Nodes
4. User Input
5. Exploration
6. Path Generation

## Dependencies
* matplotlib.pyplot
* cv2 (version 3.3)

## How to run for point robot
```
$ git clone https://github.com/varunasthana92/Dijkstra_Path_Planner.git
$ cd Dijkstra_Path_Planner
$ python2 Dijkstra_point.py
```
## How to run rigid robot
```
$ python2 Dijkstra_rigid.py
```
## Section 1: Libraries

The libraries imported for this project are:

* __numpy__ - used to handle the array data structures
* __copy__ - used to take copies of arrays into functions
* __math__ - used to generate fixed obstacles in the map
* __matplotlib.pyplot__ - used to draw the map and provide a visual
* __cv2__ - used to save the image as a JPEG
* __time__ - used to keep track of time when solving

## Section 2: Maps

The final map is defined with five obstacles and hard-coded to specific dimensions. For a point robot, the size is fixed. For a rigid robot, the obstacles expand to account for the radius and boundary, and the program then treats the problem as a point robot.

## Section 3: Actions and Nodes

Contains functions and objects to define the action set and keep track of all nodes explored. The action set includes 8 actions:

* Move up at a cost of 1
* Move left at a cost of 1
* Move right at a cost of 1
* Move down at a cost of 1
* Move up-left at a cost of square root of 2 (~ 1.414)
* Move up-right at a cost of square root of 2 (~ 1.414)
* Move down-left at a cost of square root of 2 (~ 1.414)
* Move down-right at a cost of square root of 2 (~ 1.414)


## Section 4: User Input

Generates print statements while the program is running to collect user information in the command line. When the point robot script is run, the user will be asked the following:

* Enter the initial starting coordinates h,w in integer [separated by commas]:
* Enter the goal coordinates h,w in integer [separated by commas]:

When the rigid robot script is run, the user will be asked the following:

* Enter the radius and clearance (enter 0,0 for point robot) [separated by commas]:
* Enter the initial starting coordinates h,w in integer [separated by commas]:
* Enter the goal coordinates h,w in integer [separated by commas]:

When giving the radius and clearance, the input is taken by the ceil value of radius + clearance. After giving the radius and clearance, a display map will pop up as a reference (__NOTE: The origin 0,0 is in the bottom-left. The y-axis shown is inverted. Y starts at 0 in the bottom-left corner and goes to 200 in the top-left corner__). This helps the user choose starting and goal points that are not inside an obstacle. If the user gives a point that is inside an obstacle or outside the map, the program will through an error and ask the user to re-enter the point.

## Section 5: Exploration

The code will display "Processing..." and begin searching the map from the starting location given by the user. In the file location, an image "grid_init.jpg" is saved to show the initial map with obstacles and boundary in YELLOW. While the code is running, there is an image "gridExplored.jpg" that is continuously saved/updated as the explored area increases; explored area is in RED and obstacles are in YELLOW. The worst case scenario (finding a solution across the entire map) should be solved in around 20 seconds for a point robot from 5,5 to 295,195.

If the explored area becomes blocked from reaching the goal, the program will stop exploring and the program will end with the message "No solution exist, terminating...."

## Section 6: Path Generation

After the goal point is reached, a path will be traced back from the goal to the starting point. On the map, this path will be drawn in BLUE. In the file location, an image "back_tracking.jpg" is saved. On the command line, the user can type any number and press enter to exit the program. This will close the image and the program.
