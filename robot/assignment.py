#from _future_ import print_function

import time
from sr.robot import *
from math import degrees, hypot, atan2

"""
Research Track 1, Assignment 1

Autor: Nicolas Bravi

Goal: move the tokens in the Arena

Flow Chart:
	1- search a token, if the robot can't see it, turn around 360 looking for it. If any token has not been found, exit()
	2- go to the closest token and grab it
	3- go into the Arena and release it
	4- go back and turn right
	5- restart from 1
"""



R = Robot()

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

a_arena = 5  
""" float: Threshold for the control of the linear distance with the arena"""

d_arena = 0.6
""" float: Threshold for the control of the linear distance with the arena"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0




def find_token(idMarkers):
    """
    Function to find the closest token not in a specific list
    
    Args: idMarkers (list(int)): list of code of tokens to not consider

    Returns:
    	code (int): code of the closest token (-1 if no token out of list is detected)
	dist (float): distance of the closest token (-1 if no token out of list is detected)
	rot_y (float): angle between the robot and the token (-1 if no token out of list is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and (token.info.code not in idMarkers):  # conditions to verify if there are any token in the arena.
            dist = token.dist
            rot_y = token.rot_y            
            code =  token.info.code
            
    if dist == 100:
        return -1, -1, -1
    else:
        return code, dist, rot_y



def isThereToken(idMarkers):
    """
    Function to check if there still is any token to move into the Arena
    
    Args: idMarkers (list(int)): list of code of tokens to not consider

    Returns:
    	(bool): True is there still is any token to move into the Arena, False if there is not.
    """
    for token in R.see():
        if token.info.code not in idMarkers:
            return True
            
    return False


def lookForToken(idMarkers):
    """
    Function to researh tokens if no one has been found
    
    Args: idMarkers (list(int)): list of code of tokens to not consider

    Returns:
    	(bool): True is there still is any token to move into the Arena, False if there is not.
    """
    if isThereToken(idMarkers):
        return True
    
    for i in range(25):
        turn(50, 0.1)
        if isThereToken(idMarkers):
            return True

    return False



def seeCenterArena():
    """
    Function to see how we should move to go into the Arena
    
    Returns:
    	dist (float): distance of the center of Arena
	rot_y (float): angle between the robot and the center of Arena
    """
    with R.lock:
        x, y = R.location
        heading = R.heading

    rel_x, rel_y = (-x, -y)

    dist = hypot(rel_x, rel_y)
    angle = degrees(atan2(rel_y, rel_x) - heading)
    
    #normalize
    angle = (angle + 180) % 360 - 180

    return dist, angle





def driveToArena():
    """
    Function to drive the robot to the center of Arena
    """
    dist, angle = seeCenterArena()
    
    while dist > d_arena or abs(angle) > a_arena:
        
        if dist > d_arena:
            drive(100, 0.03)
        if angle > a_arena:
            turn(60, 0.03)
        if angle< - a_arena:
            turn(-60, 0.03)
        
        dist, angle = seeCenterArena()



def driveTo(dist, angle):
    """
    Function to drive the robot to a specific point
    
    Args:
    	dist (float): distance of the point
	rot_y (float): angle between the robot and the point
    """
    
    if dist > d_th or abs(angle) > a_th:
    
        if dist > d_th:
            drive(80, 0.03)
            
        if angle > a_th:
            turn(50, 0.03)
            
        if angle < - a_th:
            turn(-50, 0.03)
    









def main():
    
    idMarkers = []
    print('--------------------------------------')
    print('START')
    print('--------------------------------------')
    
    
    while (lookForToken(idMarkers)):
    
        code, dist, rot_y = find_token(idMarkers)
        
        if code == -1:            
            continue
        
        if dist>d_th or abs(rot_y)>a_th:
            driveTo(dist, rot_y)
        else:
            R.grab()
            print('Marker ' + str(code) + ' grabbed')
            driveToArena()
            R.release()
            idMarkers.append(code)
            print('Marker '+ str(code) + ' released')
            print('')
            drive(-100,1)
            turn(90, 0.3)

    print('Job finished, ' + str(len(idMarkers)) + ' tokens moved into Arena')
    print(idMarkers)
    
    
    
    
    
    
    
    
start_time = time.time()    
main()
print("Time: ", time.time()-start_time, " seconds")







