import cv2
import Utils as utilities
from Utils import utilities
curr_angle = 90
video = cv2.VideoCapture(0)
print(cv2.__version__)
#set reolution for better fps
video.set(cv2.CAP_PROP_FRAME_WIDTH,320) # set the width to 320 p
video.set(cv2.CAP_PROP_FRAME_HEIGHT,240) # set the height to 240 p
count = 0
font = cv2.FONT_HERSHEY_SIMPLEX
size = (320,240)

result = cv2.VideoWriter('filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

while True:
    try:
            success,image = video.read()
            
            height,width,_ = image.shape
            #image_dup = utilities.region_of_interest(image,height,width)
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
            result.write(head_line)
            cv2.putText(head_line, 
                str(curr_angle), 
                (20, 20), 
                font, 1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
            count = count + 1
            print(curr_angle)
            cv2.imshow('video',head_line)
            cv2.waitKey(1)
    except KeyboardInterrupt:
            break
        
result.release()
video.release()
            
