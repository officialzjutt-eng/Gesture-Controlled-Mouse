import cv2
import mediapipe as mp
import pyautogui
import random
import os
import time
import math
import util
from pynput.mouse import Button, Controller

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

mouse = Controller()

screen_width, screen_height = pyautogui.size()


# MediaPipe Model

MODEL_PATH = "hand_landmarker.task"

BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7
)

hands = HandLandmarker.create_from_options(options)


# Variables

smooth_x, smooth_y = 0, 0
alpha = 0.25

prev_scroll_y = None


# Helpers

def get_tip(result):
    if result.hand_landmarks:
        return result.hand_landmarks[0][8]
    return None


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def move_mouse_smooth(tip):
    global smooth_x, smooth_y

    if tip is None:
        return

    x = tip.x * screen_width
    y = tip.y * screen_height

    smooth_x = smooth_x + (x - smooth_x) * alpha
    smooth_y = smooth_y + (y - smooth_y) * alpha

    pyautogui.moveTo(smooth_x, smooth_y)


# Scroll mode

def scroll_gesture(lm, frame):
    global prev_scroll_y

    fingers_distance = dist(lm[8], lm[12])

    index_open = util.get_angle(lm[5], lm[6], lm[8]) > 160
    middle_open = util.get_angle(lm[9], lm[10], lm[12]) > 160

    if fingers_distance < 0.05 and index_open and middle_open:

        cv2.putText(
            frame,
            "SCROLL MODE",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )

        y = (lm[8].y + lm[12].y) / 2

        if prev_scroll_y is not None:
            diff = y - prev_scroll_y

            if abs(diff) > 0.003:
                pyautogui.scroll(int(-diff * 2000))

        prev_scroll_y = y

    else:
        prev_scroll_y = None


# Draw hand landmarks and connections

def draw_hand(frame, lm):
    h, w, _ = frame.shape

    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (17, 18), (18, 19), (19, 20),
        (0, 17)
    ]

    for start, end in connections:
        x1 = int(lm[start].x * w)
        y1 = int(lm[start].y * h)

        x2 = int(lm[end].x * w)
        y2 = int(lm[end].y * h)

        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    for p in lm:
        x = int(p.x * w)
        y = int(p.y * h)

        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)


# Gesture detection

def detect(frame, lm, result):

    if len(lm) < 21:
        return

    draw_hand(frame, lm)

    thumb_index_dist = dist(lm[4], lm[8])
    index_tip = get_tip(result)

    # IDLE MODE (hand open)

    if util.get_angle(lm[4], lm[8], lm[12]) > 160:
        cv2.putText(
            frame,
            "IDLE",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2
        )
        return

    # MOVE MOUSE

    if thumb_index_dist < 0.08:
        move_mouse_smooth(index_tip)

    # CLICK GESTURES

    elif thumb_index_dist > 0.15:

        # LEFT CLICK
        if util.get_angle(lm[5], lm[6], lm[8]) < 50:
            mouse.click(Button.left, 1)

            cv2.putText(
                frame,
                "LEFT CLICK",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        # RIGHT CLICK
        elif util.get_angle(lm[9], lm[10], lm[12]) < 50:
            mouse.click(Button.right, 1)

            cv2.putText(
                frame,
                "RIGHT CLICK",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        # DOUBLE CLICK
        elif thumb_index_dist < 0.05:
            pyautogui.doubleClick()

    # SCROLL

    scroll_gesture(lm, frame)


# MAIN LOOP

def main():

    cap = cv2.VideoCapture(0)
    timestamp = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        timestamp += 1

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = hands.detect_for_video(mp_image, timestamp)

        lm_list = []

        if result.hand_landmarks:
            lm_list = result.hand_landmarks[0]

        detect(frame, lm_list, result)

        cv2.imshow("AI Hand Control", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()