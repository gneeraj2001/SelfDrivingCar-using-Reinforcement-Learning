def make_points(frame, line):
        height, width, _ = frame.shape
        slope, intercept = line
        y1 = height  # bottom of the frame
        y2 = int(y1 / 1.5)  # make points from middle of the frame down

        if slope == 0: 
            slope = 0.1    

        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        return [[x1, y1, x2, y2]]
