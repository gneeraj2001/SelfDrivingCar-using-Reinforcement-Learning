# SelfDrivingCar-using-Reinforcement-Learning

Objective:

The main aim of this project is to build a chassie and train it to navigate through a race course using Reinforcement Learning.

Materials Used:

      Raspberry Pi 4 board

      Raspberry Pi camera 

      Power Banks(for power supply)

      Motors

      Motor Driver

      Wheels and other hardware for the car


Sample Images of the Car:
![image](https://user-images.githubusercontent.com/91423180/201276236-33f856c4-9013-4240-8b08-5b62239cdde5.png)
![image](https://user-images.githubusercontent.com/91423180/201276393-18fc183f-32ff-4b92-b230-b86d41096708.png)


Steps Undertaken:

            1) Building the hardware of the Chassie.
           
            2) Configorating the raspberry pi Camera to detect lanes (marked using colored insulation tape)
            Opencv module was used for this.
                  Steps:
                  •	An instantaneous image of the road is captured using opencv
                  •	Perform Gaussian blur to remove noise from the captured image
                  •	Convert the image to hsv format
                  •	Perform Canny edge detection on the above image to detect lane lines
                  •	Determine the region of interest from the image(lower part) and crop out the ROI
                  •	Detect lines and slopes of the lane lines and then determine the angle at which the car is moving with respect to the lanes. (which will be used as an input           parameter to the model)

            3) The Deep Q learning Reinforcement learning algorithm was trained using the heading angle of the car as the input parameter. 
            The output gives the car 3 actions => left,straight and right based on the value of the heading angle.
                •	If the heading angle is acute then the car should correct this by steering to the left.
                •	If the heading angle is within the range 87-92 (space given for minute error) , the car should continue heading straight.
                •	If the heading angle is obtuse then the car should correct this by steering to the right.

            The car is trained using the pytorch module.

            4) Initialization of rewards for the model to learn from its mistakes.
            The rewards initialised are:
            100 if the model takes the right decision 
            -100 if the model takes the wrong decision

            The model was trained until it was able to make the right decisions (monitored)






