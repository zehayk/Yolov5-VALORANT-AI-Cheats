from typing import Counter

import keyboard
from mss import mss
import torch
import cv2
import numpy as np
import time
from pynput.mouse import Controller
from SettingsUI import SettingsUI

mouse = Controller()

import serial
# arduino = serial.Serial(port='COM10', baudrate=9600, write_timeout=1, writeTimeout=10, timeout=0)
arduino = serial.Serial(port='COM10', baudrate=115200, write_timeout=1, writeTimeout=10, timeout=0)
SENS = 1
AIM_SPEED = 1*(1/SENS)
target_multiply = [0,1.01,1.025,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05]

MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080
# MONITOR_WIDTH = 2560
# MONITOR_HEIGHT = 1440
MONITOR_SCALE = 5
region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))

device = torch.device("cuda")
# model = torch.hub.load(r'C:\proj\pypy\val-cheat\yolov5', 'custom', path=r'C:\proj\pypy\val-cheat\best.onnx', source='local').cpu()
model = torch.hub.load(r'C:\proj\pypy\val-cheat\yolov5', 'custom', path=r'C:\proj\pypy\val-cheat\best.pt', source='local').to(device)
model.conf = 0.40
model.maxdet = 10
model.apm = True
model.classes = [1]
model.eval()
model.cuda()


start_time = time.time()
x = 1
counter = 0

appUI = SettingsUI()


print(torch.cuda.is_available())

arduinoSendTime = time.time()

def arduinoCoolDown():
    print(arduinoSendTime)
    return time.time() - arduinoSendTime > 0.01


# coords:123,123!
with mss() as stc:
    while True:
        if (time.time() - start_time) > 0.5:
            arduino.reset_input_buffer()

        if appUI.isGlobalOn():
            screenshot = np.array(stc.grab(region))
            df = model(screenshot, size=736).pandas().xyxy[0]

            counter += 1
            if(time.time() - start_time) > x:
                fps = "fps:" + str(int(counter/(time.time() - start_time)))
                print(fps)
                counter = 0
                start_time = time.time()

            for i in range(0, model.maxdet):
                try:
                    xmin = int(df.iloc[i,0])
                    ymin = int(df.iloc[i,1])
                    xmax = int(df.iloc[i,2])
                    ymax = int(df.iloc[i,3])

                    # cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)

                    center = xmin + ((xmax - xmin) / 2), ymin + ((ymax - ymin) / 2)
                    # center = xmin, ymin
                    topCoords = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2))
                    finalCoords = topCoords[0] + center[0], topCoords[1] + center[1]

                    # print(finalCoords, end="")

                    # print(center)
                    # print(topCoords)
                    # print(finalCoords)
                    # print(mouse.position)
                    # move = finalCoords[0] - mouse.position[0], finalCoords[1] - mouse.position[1]
                    move = finalCoords[0] - (MONITOR_WIDTH/2), finalCoords[1] - (MONITOR_HEIGHT/2)
                    # print(move)

                    # arduino.write(f"coords:{move[0]},{move[1]}!".encode())

                    if arduinoCoolDown():
                        # txt = f"coords:{move[0]},{move[1]}!".encode()
                        txt = f"coords:{move[0] * AIM_SPEED * target_multiply[MONITOR_SCALE]},{move[1] * AIM_SPEED * target_multiply[MONITOR_SCALE]}!".encode()
                        # print("  |  " + txt)
                        print("AAAAAAAAAAAAAAAAAAAAAAA")
                        arduino.write(txt)
                        arduinoSendTime = time.time()

                except Exception as e:
                    # print(e)
                    arduino.reset_input_buffer()
                    # print("reset buffer")
                    # print("", end="")

            # cv2.imshow("frame", screenshot)
            # if (cv2.waitKey(1) == ord('l')):
            #     cv2.destroyAllWindows()
            #     break