# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 09:42:23 2021

@author: Gokul
"""

from threading import Thread
import cv2
from queue import Queue

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,800) # set the width to 320 p
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,400) # set the height to 240 p

        self.stopped = False
        self.counter =0
        self.q = Queue()
        
    def start(self):
        Thread(target=self.putFrame, args=()).start()
        return self

    def putFrame(self):

        while not self.stopped:
            self.q.put(self.stream.read())
            self.counter = self.counter + 1
            #print("Putting  = ", self.counter)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
        
    def framesize(self):
        width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT )
        print(width, height)
        
    def getFrame(self):
        return(self.q.get())
                            
    


class VideoProcess:
    """
    Class that continuously Processes a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        self.counter =0
        
    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        print("Entering showing ...")
        while not self.stopped:
            #cv2.imshow("Video", self.frame)
            
            self.counter = self.counter + 1
            print("showing  = ", self.counter)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
        

def execute_boththread(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoProcess object.
    Main thread serves only to pass frames between VideoGet and
    VideoProcess objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoProcess(video_getter.getFrame()).start()
    
    while True:
        video_shower.frame = video_getter.getFrame()
    
    



if __name__ == '__main__':
    execute_boththread(source=0)