import numpy as np

# angle (FIXED for MediaPipe Tasks)
def get_angle(a, b, c):
    radians = np.arctan2(c.y - b.y, c.x - b.x) - np.arctan2(a.y - b.y, a.x - b.x)
    angle = np.abs(np.degrees(radians))

    if angle > 180:
        angle = 360 - angle

    return angle



# distance (FIXED)
def get_distance(landmark_list):
    if len(landmark_list) < 2:
        return 0

    a = landmark_list[0]
    b = landmark_list[1]

    L = np.hypot(b.x - a.x, b.y - a.y)

    return np.interp(L, [0, 1], [0, 1000])