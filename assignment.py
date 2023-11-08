#from _future_ import print_function

from math import degrees, hypot, atan2
import time
from sr.robot import *


R = Robot()

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""


a_arena = 5  # Threshold for the control of the linear distance with the arena
d_arena = 0.6  # Threshold for the control of the linear distance with the arena


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
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
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
    #for token in R.see():
     #   if not (token.info.code in idMarkers):
     #       return True
    code,_,_ = find_token(idMarkers) 
    return code>0


def lookForToken(idMarkers):
    
    if isThereToken(idMarkers):
        return True
    
    for i in range(12):
        turn(50, 0.15)
        if isThereToken(idMarkers):
            return True

    return False



def seeCenterArena():
    with R.lock:
        x, y = R.location
        heading = R.heading

    rel_x, rel_y = (-x, -y)

    dist = hypot(rel_x, rel_y)
    angle = degrees(atan2(rel_y, rel_x) - heading)
    
    #normalize
    angle = (angle + 180) % 360 - 180

    return dist, angle




#TODO
def driveToArena():
    dist, angle = seeCenterArena()
    
    while dist > d_arena or abs(angle) > a_arena:
        
        if dist > d_arena:
            drive(80, 0.03)
        if angle > a_arena:
            turn(60, 0.03)
        if angle< - a_arena:
            turn(-60, 0.03)
        
        dist, angle = seeCenterArena()



# TODO
def driveTo(dist, angle):
    
    if dist > d_th or abs(angle) > a_th:
    
        if dist > d_th:
            drive(80, 0.035)
            
        if angle > a_th:
            turn(60, 0.03)
            
        if angle < - a_th:
            turn(-60, 0.03)
    









def main():
    
    idMarkers = []
    print('Marker aoo')
    
    #drive(100, 0.3)
    
    while (lookForToken(idMarkers)):
    
        code, dist, rot_y = find_token(idMarkers)
        
        if dist>d_th or abs(rot_y)>a_th:
            driveTo(dist, rot_y)
        else:
            R.grab()
            #print(f'Marker {code} grabbed')
            #print('Marker grabbed', code)
            driveToArena()
            R.release()
            idMarkers.append(code)
            #print(f'Marker {code} released')
            #print('Marker released', code)
            drive(-100,1)
            turn(100, 0.3)

    print('Job finished, {len(idMarkers)} moved in Arena')
    print(idMarkers)
    
    
    
    
    
    
    
main()







