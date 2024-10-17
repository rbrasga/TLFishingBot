import cv2
import pyautogui
import time
import random
import mss
import numpy as np
from PIL import Image

class FishBot:

    def __init__(self):
        self.snapRegion = {"mon": 1, "top": 900, "left": 1248, "width": 32, "height": 32}
        self.castRegion = {"mon": 1, "top": 841, "left": 1524, "width": 25, "height": 25}
        self.recoverRegion = {"mon": 1, "top": 805, "left": 1525, "width": 24, "height": 24}
        self.fishRegion = {"mon": 1, "top": 782, "left": 1450, "width": 13, "height": 143}
        self.staminaRegion = {"mon": 1, "top": 784, "left": 1475, "width": 8, "height": 138}
        self.sct = mss.mss()

    def screenGrab(self, region):
        try:
            return np.array(self.sct.grab(region))
        except Exception as e:
            print(f"[Error] Unable to take screenshot: {region}. {e}")
            return None

    def drawBoxes(self, frame):
        regions = [
            ("Snap", self.snapRegion),
            ("Cast", self.castRegion),
            ("Recover", self.recoverRegion),
            ("Fish", self.fishRegion),
            ("Stamina", self.staminaRegion),
        ]
        for name, region in regions:
            top_left = (region["left"], region["top"])
            bottom_right = (region["left"] + region["width"], region["top"] + region["height"])
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(frame, name, (top_left[0], top_left[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (0, 255, 0), 1, cv2.LINE_AA)

    def main(self):
        cv2.namedWindow("Visuals", cv2.WINDOW_NORMAL)

        while True:
            # Capture the entire screen to draw boxes over it
            monitor = self.sct.monitors[4]
            frame = np.array(self.sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert to BGR for OpenCV

            # Draw the bounding boxes on the frame
            self.drawBoxes(frame)

            # Display the frame with regions
            cv2.imshow("Visuals", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

# Runs the main function
if __name__ == '__main__':
    f = FishBot()
    f.main()