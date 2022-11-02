# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 09:46:39 2021

@author: gopal.alc
"""


import RPi.GPIO as GPIO  
import math
import time     # this lets us have a time delay (see line 12)
import datetime


pulse_left = 0
pulse_right = 0
starttime_left = 0
endtime_left = 0
starttime_right = 0
endtime_right = 0
deltatime_left = 0
deltatime_right = 0


deltatime_right_buff =[]
right_index=0

itretor_left = 1
itretor_right = 1



speed_left =0.0
speed_right = 0.0

r_cm = 3.5

GPIO.setwarnings(False)
#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)

left_pwm =  12
right_pwm = 12

inA1 = 12
inA2 = 11
inB1 = 15
inB2 = 16
Enable1 = 18
Enable2 = 19

leftwhl_pulse = 29   #35
rightwhl_pulse = 31   #36


GPIO.setup(Enable1,GPIO.OUT) #ENA
GPIO.setup(Enable2,GPIO.OUT) #ENB
GPIO.setup(inA1,GPIO.OUT)
GPIO.setup(inA2,GPIO.OUT)
GPIO.setup(inB1,GPIO.OUT)
GPIO.setup(inB2,GPIO.OUT)

#Defining PWM
motor1pwm = GPIO.PWM(Enable1, 100)
motor2pwm = GPIO.PWM(Enable2, 100)
  

# Pin 29 and 31 are set up as input pins to receive pulse from Speed Enoder

GPIO.setup(leftwhl_pulse, GPIO.IN)
GPIO.setup(rightwhl_pulse, GPIO.IN)


class RingBuffer:
    def __init__(self, size):
        self.data = [None for i in range(size)]
        self.n = size

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data
    
    def avg_data(self):
        temp =0.0
        for value in self.data:
            temp = temp + value
        return (temp/self.n)
buffer_size = 5
buf_left = RingBuffer(buffer_size)
buf_right = RingBuffer(buffer_size)

# when a changing edge is detected on port 25 and 26, regardless of whatever   
# else is happening in the program, the function Pulsetimer_Leftwheel and 
# Pulsetimer_Rightwheel will be run  




# Define a threaded callback function to run in another thread when events are detected  
def Pulsetimer_Leftwheel(channel):  
    global pulse_left, starttime_left, endtime_left, deltatime_left, last_task_time_left
    global itretor_left

    if pulse_left == 20:
        pulse_left = 0

        endtime_left = time.time()
        buf_left.append(endtime_left - starttime_left)
        if itretor_left <= buffer_size :
            deltatime_left = endtime_left - starttime_left
            itretor_left = itretor_left + 1
        else:
            deltatime_left = buf_left.avg_data()
             
        starttime_left= time.time()
#         print(deltatime_left)

    else:
        pulse_left = pulse_left + 1
    #print('pulse left is ',pulse_left)


def Pulsetimer_Rightwheel(channel):  
    global pulse_right, starttime_right, endtime_right, deltatime_right, last_task_time_right
    global itretor_right

    if pulse_right == 20:
        pulse_right = 0

        endtime_right = time.time()
        buf_right.append(endtime_right - starttime_right)
        if itretor_right <= buffer_size :
            deltatime_right = endtime_right - starttime_right
            itretor_right = itretor_right + 1
        else:
            deltatime_right = buf_right.avg_data()
             
        starttime_right= time.time()
#         print(deltatime_right)

    else:
        pulse_right = pulse_right + 1
    #print('pulse left is ',pulse_left)





    


GPIO.add_event_detect(leftwhl_pulse, GPIO.RISING, callback=Pulsetimer_Leftwheel)
GPIO.add_event_detect(rightwhl_pulse, GPIO.RISING, callback=Pulsetimer_Rightwheel)


def calculate_speed():
    global pulse_left, pulse_right, starttime_left, endtime_left, starttime_right, endtime_right,speed_left, speed_right, r_cm
    km_per_hour_left =0.0
    km_per_hour_right = 0.0
    
    
    circ_cm = (2*math.pi)*r_cm
    dist_km = circ_cm/100000
    
    #print(deltatime_left, deltatime_right)
    
    if deltatime_left !=0:
        rpm_left = 1/deltatime_left *60
        km_per_sec_left = dist_km / deltatime_left		# calculate KM/sec
        km_per_hour_left = km_per_sec_left * 3600
        
    if deltatime_right !=0:
        rpm_right = 1/deltatime_right *60
        km_per_sec_right = dist_km / deltatime_right		# calculate KM/sec
        km_per_hour_right = km_per_sec_right * 3600
         
    return km_per_hour_left,  km_per_hour_right
    
########action to move straight########
def moveForward():
    
    global left_pwm
    global right_pwm
    global inA1
    global inA2
    global inB1
    global inB2

    motor1pwm.start(right_pwm)
    GPIO.output(inA1,True)
    GPIO.output(inA2,False)#forward   #right
    motor2pwm.start (left_pwm)
    GPIO.output(inB1,True)#forward  #left
    GPIO.output(inB2,False)
    time.sleep(1)


if __name__ == '__main__':
    try:
        while True:
            moveForward() 
            left_kmph , right_kmph = calculate_speed()
            print(left_kmph,',', right_kmph )
            
    except KeyboardInterrupt:
        GPIO.cleanup() 
        print('You cancelled the operation')

    