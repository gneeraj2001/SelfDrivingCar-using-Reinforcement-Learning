import time, sys
import RPi.GPIO as GPIO
from ai import Dqn
import Utils as utilities
import cv2 
import numpy as np 
from Utils import utilities


curr_angle = 90
brain = Dqn(1,3,0.9)    #the brain(ai) object
last_reward = 0 #initialising the last reward
score = []
dirl = 0
dirr = 0
dirs = 0
straight_lower = 88
straight_higher = 92
count = 0
font = cv2.FONT_HERSHEY_SIMPLEX
########### Motor functions for the car#############

GPIO.setwarnings(False)
#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)

check = 0
left_pwm = 11
right_pwm = 11

left_pwm_turn = 8
right_pwm_turn = 8
inA1 = 12
inA2 = 11
inB1 = 15
inB2 = 16
Enable1 = 19
Enable2 = 18


GPIO.setup(Enable1,GPIO.OUT) #ENA
GPIO.setup(Enable2,GPIO.OUT) #ENB
GPIO.setup(inA1,GPIO.OUT)
GPIO.setup(inA2,GPIO.OUT)
GPIO.setup(inB1,GPIO.OUT)
GPIO.setup(inB2,GPIO.OUT)

#Defining PWM
motor1pwm = GPIO.PWM(Enable1, 100) #left
motor2pwm = GPIO.PWM(Enable2, 100) #right

size = (320,240)

result = cv2.VideoWriter('filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)



########action to move straight########
def action_go_straight():
    
    global left_pwm
    global right_pwm
    global inA1
    global inA2
    global inB1
    global inB2


    motor1pwm.start(left_pwm)
    GPIO.output(inA1,True)
    GPIO.output(inA2,False)#forward
    motor2pwm.start (right_pwm)
    GPIO.output(inB1,True)#forward
    GPIO.output(inB2,False)
    print('moving straight')
    #time.sleep(1)
    
    
########action to move left###########
def action_go_left(): 
    
    global left_pwm
    global right_pwm
    global inA1
    global inA2
    global inB1
    global inB2


    motor1pwm.start(left_pwm_turn)
    GPIO.output(inA1,False)
    GPIO.output(inA2,False)#forward
    motor2pwm.start (right_pwm_turn)
    GPIO.output(inB1,True)#forward
    GPIO.output(inB2,False)
    print('moving left')
    #time.sleep(0.005)

########action to move right###########
def action_go_right(): 
    
    global left_pwm
    global right_pwm
    global inA1
    global inA2
    global inB1
    global inB2


    motor1pwm.start(left_pwm_turn)#left
    GPIO.output(inA1,False)
    GPIO.output(inA2,True)#forward
    motor2pwm.start (right_pwm_turn)#right
    GPIO.output(inB1,False)#forward
    GPIO.output(inB2,False)
    print('moving right')
    #time.sleep(0.005)

def action_stop():
    
    global left_pwm
    global right_pwm
    global inA1
    global inA2
    global inB1
    global inB2


    motor1pwm.start(left_pwm)
    GPIO.output(inA1,False)
    GPIO.output(inA2,True)#forward
    motor2pwm.start (right_pwm)
    GPIO.output(inB1,False)#forward
    GPIO.output(inB2,False) 

##### For the first action
def first_action(angle):
    
    
    if (angle > 87 and angle < 92):
        action_go_straight()
        
    
    else:
        print("havent placed at 90 degrees")
        

###### moves based on the action######
def move(action):

    if action is 0: #go straight
        action_go_straight()
    
    elif action is 1: #go left
        action_go_left()

    else: # go right
        action_go_right()

'''
    angle > 90(range) the robot is moving towards the left,to correct it has to move to the right
    angle < 90(range) the robot is moving towards the right,to correct it has to move to the left
    angle is within the range(87-92) the robot is moving straight and has to continue straight
    
    action = 0 straight
    action = 1 move left
    action = 2 move right

'''
######### To get reward value ######
def reward_ai(angle,action):    
    
    
    if angle > 95 and action == 2:
        rwd = 100
        check = 1
    
    elif (angle > 95 and (action == 0 or action == 1)):
        rwd = -100
        action_go_right()
        check = 0
    
    elif angle < 87 and action == 1:
        rwd = 100
        check = 1
    
    elif (angle < 87 and (action == 0 or action == 2)):
        rwd = -100
        action_go_left()
        check = 0
        
    elif angle > 87 and angle < 95 and action == 0:
        rwd = 100
        check = 1
        
    elif angle > 87 and angle < 95 and action is not 0:
        rwd = -100
        action_go_straight()
        check = 0
    else:
        rwd = 0
        check = 0
    return rwd,check

#########updates the ai########
def update(steering_angle):
    global brain
    global last_reward
    global dirl
    global dirr
    global dirs
    global straight_lower 
    global straight_higher
    global check
    
    
    '''
    if steering_angle > 88 or steering_angle <92:
        dirl = 0
        dirs = 1
        dirr = 0

    elif steering_angle > 90:
        dirl = 1
        dirs = 0
        dirr = 0

    else:
        dirl = 0
        dirs = 0
        dirr = 1
    
    '''

    
    angle = steering_angle/180.0   #normalising for the ai(dqn)
    last_signal = [angle]          #input stae to the network
    action = brain.update(last_signal, last_reward)
    last_reward,check = reward_ai(steering_angle,action.item())
    
    #last_reward,check = reward_ai(steering_angle,action.item())
    #last_signal = [angle]
    #score.append(brain.score())
    
    if check is 1:
        move(action.item())
    
    
    #print(last_signal , action.item(),last_reward, check)


if __name__ == '__main__':
    

    brain.load()
    
    '''
    motor1pwm.start(left_pwm)
    GPIO.output(inA1,False)
    GPIO.output(inA2,True)#forward
    motor2pwm.start (right_pwm)
    GPIO.output(inB1,True)#forward
    GPIO.output(inB2,False)
    '''
    
########
# capture video from raspberry pi camera
    video = cv2.VideoCapture(0)
    
    #set reolution for better fps
    video.set(cv2.CAP_PROP_FRAME_WIDTH,320) # set the width to 320 p
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,240) # set the height to 240 p
    

    try:
        while True:

            success,image = video.read()
            
            height,width,_ = image.shape
            image_dup = utilities.region_of_interest(image,height,width)
            #hsv_image = utilities.convert_to_hsv(image)
            blur_image = utilities.gaussian_blur(image)
            canny_image = utilities.edge_detection(blur_image)
            roi = utilities.region_of_interest(canny_image,height,width)
            road_lane = utilities.detect_line_segments(roi)
            
            lane_lines = utilities.average_slope_intercept(image,road_lane)
            lane_lines_image = utilities.display_lines(image,lane_lines)
            new_angle = utilities.get_steering_angle(lane_lines_image,lane_lines)
            curr_angle = utilities.stabilize_steering_angle(curr_angle, new_angle, len(lane_lines))
            head_line = utilities.display_heading_line(lane_lines_image,curr_angle)
            #angle = utilities.get_steering_angle(lane_lines_image, lane_lines)
            result.write(image)
            
            cv2.putText(head_line, 
                str(curr_angle), 
                (20, 20), 
                font, 1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
            '''
            if lane_lines == []:
                print('stopped')
                action_stop()
                GPIO.cleanup()
            
             if count % 2 == 0:
                 action_go_straight()
                 count = count + 1
             else:
                 update(angle)
                 count = count + 1
            
            '''
            update(curr_angle)
            cv2.imshow('VID',head_line)
            print((curr_angle))
            key = cv2.waitKey(1)
            
            
                
                
    except KeyboardInterrupt:
        brain.save()
        GPIO.cleanup()
        video.release()
        print('Saving ')
        result.release()
        video.release()
        cv2.destroyAllWindows()
    
    

    
    
    