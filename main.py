import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf')

import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
from pynput.keyboard import Controller

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Define the keys layout including spacebar
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["SPACE"]]

finalText = ""

# Initialize the keyboard controller
keyboard = Controller()


# Define the Button class
class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


# Function to draw buttons on the screen
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        if button.text == "SPACE":
            cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)  # Green background for space bar
            cv2.putText(img, button.text, (x + 110, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)  # Black text
        else:
            cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)  # Green background
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)  # Black text
    return img


# Create the button list
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == "SPACE":
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, [500, 85]))
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img)

    img = drawAll(img, buttonList)

    if hands:
        hand = hands[0]
        lmList = hand['lmList']

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)  # Black text

                # Calculate the distance between index finger tip (landmark 8) and middle finger tip (landmark 12)
                l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

                if l < 30:
                    keyboard.press(button.text if button.text != "SPACE" else " ")
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 165, 255), cv2.FILLED)  # Orange background
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0),
                                4)  # Black text
                    finalText += button.text if button.text != "SPACE" else " "
                    sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


