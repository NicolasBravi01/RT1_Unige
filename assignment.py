#from _future_ import print_function

import time
from sr.robot import *
from math import degrees, hypot, atan2





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
        code =  token.info.code
        if token.dist < dist and not (code in idMarkers):  # conditions to verify if there are any token in the arena.
            dist = token.dist
            rot_y = token.rot_y
            
    if dist == 100:
        return -1, -1, -1
    else:
        return code, dist, rot_y



def isThereToken(idMarkers):
    """
    Function to check if there still is any token to move in Arena
    
    Args: idMarkers (list(int)): list of code of tokens to not consider

    Returns:
    	(bool): True is there still is any token to move in Arena, False if there is not.
    """
    for token in R.see():
        if not (token.info.code in idMarkers):
            return True
            
    return False


def lookForToken(idMarkers):
    """
    Function to researh tokens if no one has been found
    
    Args: idMarkers (list(int)): list of code of tokens to not consider

    Returns:
    	(bool): True is there still is any token to move in Arena, False if there is not.
    """
    if isThereToken(idMarkers):
        return True
    
    for i in range(12):
        turn(50, 0.15)
        if isThereToken(idMarkers):
            return True

    return False



def seeCenterArena():
    """
    Function to see how we should move to go in Arena
    
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



# TODO
def driveTo(dist, angle):
    """
    Function to drive the robot to a specific point
    
    Args:
    	dist (float): distance of the point
	rot_y (float): angle between the robot and the point
    """
    
    if dist > d_th or abs(angle) > a_th:
    
        if dist > d_th:
            drive(100, 0.03)
            
        if angle > a_th:
            turn(60, 0.03)
            
        if angle < - a_th:
            turn(-60, 0.03)
    









def main():
    
    idMarkers = []
    print('--------------------------------------')
    print('START')
    print('--------------------------------------')
    
    
    while (lookForToken(idMarkers)):
    
        code, dist, rot_y = find_token(idMarkers)
        
        if dist>d_th or abs(rot_y)>a_th:
            driveTo(dist, rot_y)
        else:
            R.grab()
            print('Marker ' + str(code) + ' grabbed')
            driveToArena()
            R.release()
            idMarkers.append(code)
            print('Marker '+ str(code) + ' released')
            print()
            drive(-100,1)
            turn(80, 0.3)

    print('Job finished, ' + str(len(idMarkers)) + ' moved in Arena')
    print(idMarkers)
    
    
    
    
    
    
    
main()







