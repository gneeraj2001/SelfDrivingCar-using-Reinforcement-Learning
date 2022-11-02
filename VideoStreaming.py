# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 08:13:47 2021


"""

from threading import Thread, Lock
import cv2
import queue as Q
import numpy as np
import logging

#Class to stream Camera live
class CameraStream(object):
    def __init__(self, src=0):
        #self.stream = cv2.VideoCapture(src)

        #(self.grabbed, self.frame) = self.stream.read()
       
        self.stream = cv2.VideoCapture(0)
        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,640) # set the width to 320 p
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        
        
        self.started = False
        self.read_lock = Lock()
        self.q = Q.Queue()
        logging.debug('Creating CameraStream object .....')
        #print("Creating CameraStream object .....")

    def start(self):
        if self.started:
            logging.debug('Already started CameraStream object .....')
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        logging.debug('Started Streaming thread .....')
        #print("Started Streaming thread .....")
        return self

    def update(self):
        logging.debug('Entering Streaming thread.....')
        while self.started:
            #(grabbed, frame) = self.stream.read()
            logging.debug('Running Streaming thread.....')
            grabbed, frame = self.stream.read()
            if np.shape(frame) == ():
                self.stop()
                logging.debug('Null Frame:  Streaming thread.....')
            
            #print("Running Streaming thread.....")
            self.read_lock.acquire()

            self.grabbed, self.frame = grabbed, frame
            self.q.put(frame)
            self.read_lock.release()
            

    def read(self):
        logging.debug('Inside Read function .....')

        frame_q = self.q.get()

        return frame_q

    def stop(self):
        self.started = False
        logging.debug('Stopping Streaming Thread ....')


    def __exit__(self, exc_type, exc_value, traceback):
        logging.debug('Releasing Streaming object.....')
        self.stream.release()
        

        
# function to instatiate start and execute both threads        
def execute_stream_thread():
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    stream = CameraStream().start()

    while stream.q.not_empty:
        logging.debug(' Inside while loop  ......')
        frame = stream.read()

        if np.shape(frame) == ():

            logging.debug(' stopping all Processess ......  ......')
            stream.stop()
            #cv2.destroyAllWindows()
            break
        else:
            logging.debug('Showing Image ......')
            cv2.imshow('Live stream', frame)
            if cv2.waitKey(1) == 27 :
                break
    logging.debug(' Out of while loop stopping all Threads ......')
 
    
    
    
    
#Main Function

if __name__ == '__main__':
    execute_stream_thread()
    