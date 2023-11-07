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
    for token in R.see():
        if not (token.info.code in idMarkers):
            return True
    return False


def lookForToken(idMarkers):
    
    if isThereToken(idMarkers):
        return True
    
    for i in range(7):
        turn(50, 0.01)
    
    if isThereToken(idMarkers):
        return True

    for i in range(14):
        turn(-50, 0.01)

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
    
    while dist < d_arena or abs(angle) < a_arena:
        
        if dist < d_arena:
            drive(80, 0.035)
        if angle > a_arena:
            drive(60, 0.03)
        if angle< - a_arena:
            drive(-60, 0.03)
        
        dist, angle = seeCenterArena()



# TODO
def driveTo(dist, angle):
    
    if dist < d_th or abs(angle) < a_th:
        if dist < d_th:
            drive(80, 0.035)
        if angle > a_th:
            drive(60, 0.03)
        if angle < - a_th:
            drive(-60, 0.03)
    









def main():
    
    idMarkers = []
    
    while (lookForToken(idMarkers)):
        code, dist, rot_y = find_token(idMarkers)
        
        if dist<d_th or abs(rot_y)<a_th:
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
            drive(-100, 0.5)
            turn(100, 0.2)

    #print('Job finished, {len(idMarkers)} moved in Arena')
    #print(idMarkers)
    
    
    
    
    
    
    
    
main()








"""
v = []
dist_arena, rot_arena = seeCenterArena()  # look for the center of arena.

while 1:

    dist_arena = dist_arena + 0.5;

    markers = R.see()
    for m in markers:
        v = v

    dist, rot_y = find_token_color(v)  # we look for markers.

    if dist == -1:
        print("I don't see any token!!")
        turn(45, 0.5)

    elif dist < d_th:

        print("Found it!")

        grabbed = R.grab()  # if we are close to the token, we grab it.

        v.append(m.info.code)  # put into the vector v the code of the marker grabbed.

        print("Gotcha!")

        while (d_arena < dist_arena or 0.4 < abs(rot_arena)) and grabbed is True:

            dist_arena, rot_arena = seeCenterArena()

            if rot_arena < -a_th:

                turn(-10, 0.25)  # turn left if the robot can't see the center of arena

            elif rot_arena > a_th:

                turn(+10, 0.25)  # turn right if the robot can't see the center of arena

            elif -a_th <= rot_arena <= a_th:  # if the robot is well aligned with the token, we go forward

                drive(50, 0.5)

            if d_arena > dist_arena:
                grabbed = R.release()  # release the marker when the robot is in the center of arena
                grabbed = False
                print("Box released" + str(grabbed))

                drive(-50, 1)

                turn(-35, 1)


    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(50, 0.5)

    elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-5, 0.25)

    elif rot_y > a_th:
        print("Right a bit...")
        turn(+5, 0.25)

    box = R.see()  # control if there are any token in the arena

    if not box:
        turn(15, 0.5)
        if not box:
            turn(400, 1)
            if not box:
                exit()
"""
