from typing import Counter
from mss import mss
import torch
import cv2
import numpy as np
import time
import math
import keyboard
# import mouse
import threading
import pyautogui
import win32api, win32con
import torchvision.transforms as transforms



def cooldown(cooldown_bool, wait):
    time.sleep(wait)
    cooldown_bool[0] = True


MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080
MONITOR_SCALE = 5
region = (int(MONITOR_WIDTH / 2 - MONITOR_WIDTH / MONITOR_SCALE / 2),
          int(MONITOR_HEIGHT / 2 - MONITOR_HEIGHT / MONITOR_SCALE / 2),
          int(MONITOR_WIDTH / 2 + MONITOR_WIDTH / MONITOR_SCALE / 2),
          int(MONITOR_HEIGHT / 2 + MONITOR_HEIGHT / MONITOR_SCALE / 2))
x, y, width, height = region
screenshot_center = [int((width - x) / 2), int((height - y) / 2)]
triggerbot = False
triggerbot_toggle = [True]

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
device = torch.device("cuda")

ssd_model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd')
utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd_processing_utils')
model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd', path=r'C:\proj\pypy\val-cheat\best.pt').eval().to(device)
# model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd', model_math=4, path=r'C:\proj\pypy\val-cheat\best.pt', source='local').eval().to(device)

# model.conf = 0.40
model.maxdet = 10
model.apm = True
model.classes = [0]

transform = transforms.ToTensor()

start_time = time.time()
x = 1
counter = 0


def actual_coords(coordX, coordY):
    return ((((MONITOR_WIDTH/2) / 5) * 4) + coordX), ((((MONITOR_HEIGHT/2) / 5) * 4) + coordY)


with mss() as stc:
    while True:
        startTimeWhileTrue = time.time()
        a = time.time()
        closest_x = 0
        closest_y = 0

        closest_part_distance = 100000
        closest_part = -1
        print(time.time() - a)
        a = time.time()
        screenshot = np.array(stc.grab(region))
        print(f"screenshot: {time.time() - a}")
        a = time.time()
        rgb_image = screenshot[:, :, :3]
        tensor_segment = transform(rgb_image)
        df = model(tensor_segment.to(device))  #.pandas().xyxy[0]  # , size=736
        print(f"model shit: {time.time() - a}")

        a = time.time()
        counter += 1
        if (time.time() - start_time) > x:
            fps = "fps:" + str(int(counter / (time.time() - start_time)))
            print(fps)
            counter = 0
            start_time = time.time()
            # exit(0)
        print(f"hein: {time.time() - a}")

        a = time.time()
        for i in range(0, model.maxdet):
            try:
                xmin = int(df.iloc[i, 0])
                ymin = int(df.iloc[i, 1])
                xmax = int(df.iloc[i, 2])
                ymax = int(df.iloc[i, 3])

                centerX = (xmax - xmin) / 2 + xmin
                centerY = (ymax - ymin) / 2 + ymin

                distance = math.dist([centerX, centerY], screenshot_center)

                aX, aY = actual_coords(centerX, centerY)
                # print(f"coords: {centerX}. {centerY}")
                # print(f"real coords: {aX}. {aY}")


                if int(distance) < closest_part_distance:
                    closest_part_distance = distance
                    closest_part = i
                    closest_x = aX
                    closest_y = aY

                # cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)
            except:
                print("", end="")
        print(f"for: {time.time() - a}")

        # a = time.time()
        # cv2.imshow("frame", screenshot)
        # print(f"cv2.imshow: {time.time() - a}")

        # if mouse.is_pressed(button='left') and triggerbot:
        #     try:
        #         # pyautogui.moveRel(100, 100)
        #         win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 100, 0, 0, 0)
        #         print("aaa")
        #     except Exception as e:
        #         print(e)

        # if keyboard.is_pressed('`'):
        #     triggerbot = not triggerbot
        #     print(triggerbot)
        #     # if triggerbot_toggle[0] == True:
        #     #     triggerbot = not triggerbot
        #     #     print(triggerbot)
        #     #     triggerbot_toggle[0] = False
        #         # thread = threading.Thread(target=cooldown, args=(triggerbot_toggle, 0.2,))
        #         # thread.start()
        #
        # if closest_part != -1:
        #     xmin = df.iloc[closest_part, 0]
        #     ymin = df.iloc[closest_part, 1]
        #     xmax = df.iloc[closest_part, 2]
        #     ymax = df.iloc[closest_part, 3]
        #     if triggerbot and screenshot_center[0] in range(int(xmin), int(xmax)) and screenshot_center[1] in range(int(ymin), int(ymax)):
        #         keyboard.press_and_release("k")
        #         print("", end="")

        # a = time.time()
        # if(cv2.waitKey(1) == ord('l')):
        #     cv2.destroyAllWindows()
        #     break
        # print(f"key destroy: {time.time() - a}")

        print(f"total time: {time.time() - startTimeWhileTrue}")