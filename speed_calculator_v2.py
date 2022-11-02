# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 09:46:39 2021

@author: gopal.alc
"""


import RPi.GPIO as GPIO  
import time     # this lets us have a time delay (see line 12)



pulse_left = 0
pulse_right = 0
starttime_left = 0
endtime_left = 0
starttime_right = 0
endtime_right = 0
deltatime_left = 0
deltatime_right = 0


itretor_left = 1
itretor_right = 1


# PID Parameters initialization ######
previous_time =0.0  
previous_error=0.0  
Integral=0.0             
D_cycal=10  
Kp=2.05                                       # Proportional controller Gain (0 to 100)  
Ki=0                                       # Integral controller Gain (0 to 100)  
Kd=1.3                                      # Derivative controller Gain (0 to 100) 

######################################

GPIO.setwarnings(False)
#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)

left_pwm =  14
right_pwm = 10

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
buffer_size = 10
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

#This event triggers a call to function to calculate he pulses everytime
# there is a rising edge

GPIO.add_event_detect(leftwhl_pulse, GPIO.RISING, callback=Pulsetimer_Leftwheel)
GPIO.add_event_detect(rightwhl_pulse, GPIO.RISING, callback=Pulsetimer_Rightwheel)


def calculate_rpm():
    global pulse_left, pulse_right, starttime_left, endtime_left, starttime_right, endtime_right    
    rpm_left = 0
    rpm_right = 0
    
  
    #print(deltatime_left, deltatime_right)
    
    if deltatime_left !=0:
        rpm_left = 60/deltatime_left
        
    if deltatime_right !=0:
        rpm_right = 60/deltatime_right
        
        
    return rpm_left,  rpm_right



##########PID Function ################

def PID_function(set_rpm, feedback):  
      
    global previous_time  
    global previous_error  
    global Integral  
    global D_cycal  
    global Kp  
    global Ki  
    global Kd  
      
    error = set_rpm - feedback                    # Differnce between expected RPM and run RPM  
      
    if (previous_time== 0):  
         previous_time =time.time()  
           
    current_time = time.time()  
    delta_time = current_time - previous_time  
    delta_error = error - previous_error  
      
    Pout = (Kp/10 * error)                
      
    Integral += (error * delta_time)  
      
      
    if Integral>10:        
        Integral=10  
          
    if Integral<-10:  
        Integral=-10  
      
    Iout=((Ki/10) * Integral)  
      
      
    Derivative = (delta_error/delta_time)         #de/dt  
    previous_time = current_time  
    previous_error = error  
      
    Dout=((Kd/1000 )* Derivative)  
      
    output = Pout + Iout + Dout                  # PID controller output
    
      
    if ((output>D_cycal)&(D_cycal<15)):             
        D_cycal+=0.1  
          
    if ((output<D_cycal)&(D_cycal>5)):             
        D_cycal-=0.1
        
    print(set_rpm, feedback, error, output, D_cycal)
#    print(Pout,Iout,Dout)
    return(D_cycal)
        
        
#######################################
    
########action to move straight########

def moveForward(_pwm_value):
    
    global left_pwm
    global right_pwm
    global inA1
    global inA2
    global inB1
    global inB2

    # Right motor control
#    motor1pwm.start(right_pwm)
    motor1pwm.ChangeDutyCycle(_pwm_value)
    GPIO.output(inA1,False)
    GPIO.output(inA2,True)#forward   #right

    
    # Left motor control
#    motor2pwm.start (left_pwm)
#     motor2pwm.ChangeDutyCycle(left_pwm)
#     GPIO.output(inB1,False)#forward  #left
#     GPIO.output(inB2,True)
    time.sleep(0.05)



def starttomove(_pwm_value):
    
    global left_pwm
    global right_pwm
    global inA1
    global inA2
    global inB1
    global inB2

    # Right motor control
#    motor1pwm.start(right_pwm)
    motor1pwm.start(_pwm_value)
    GPIO.output(inA1,False)
    GPIO.output(inA2,True)#forward   #right

    
    # Left motor control
#    motor2pwm.start (left_pwm)
    motor2pwm.start(left_pwm)
    GPIO.output(inB1,False)#forward  #left
    GPIO.output(inB2,True)
    time.sleep(0.05)

#####  Main Function Call #############

if __name__ == '__main__':
    try:
        starttomove(10)
        time.sleep(2)
        while True:
            
            left_ , right_ = calculate_rpm()
            pwm_value = PID_function(left_, right_)
            #print(left_,',', right_ )
            #moveForward(14) 
            
            
    except KeyboardInterrupt:
        GPIO.cleanup() 
        print('You cancelled the operation')

    