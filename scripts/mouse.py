# import tkinter as tk
# from tkinter import ttk
# import sv_ttk
#
# def update_selection():
#     selection = selected_option.get()
#     # label.config(text=f"Selected option: {selection}")
#     if selection == options[2]:
#         strength_scale.config(state=tk.NORMAL)
#         soft_aim_label.config(state=tk.NORMAL)
#         strength_value_label.config(state=tk.NORMAL)
#     else:
#         strength_scale.config(state=tk.DISABLED)
#         soft_aim_label.config(state=tk.DISABLED)
#         strength_value_label.config(state=tk.DISABLED)
#
# def update_strength_scale(value):
#     strength_value_label.config(text=int(float(value)))
#
# def toggle_global():
#     if var.get():  # If Global is selected
#         for radio_button in radio_buttons:
#             radio_button.config(state=tk.NORMAL)
#
#         if selected_option.get() == options[2]:
#             strength_scale.config(state=tk.NORMAL)
#             soft_aim_label.config(state=tk.NORMAL)
#             strength_value_label.config(state=tk.NORMAL)
#     else:
#         for radio_button in radio_buttons:
#             radio_button.config(state=tk.DISABLED)
#         strength_scale.config(state=tk.DISABLED)
#         soft_aim_label.config(state=tk.DISABLED)
#         strength_value_label.config(state=tk.DISABLED)
#         # selected_option.set("Off")  # Reset selected option when Global is turned off
#
# # Create the main window
# window = tk.Tk()
# window.title("SettingsUI")
#
# # Set the window size (width x height)
# window.geometry("400x300")
#
# # Create a variable to store the state of the toggle
# var = tk.BooleanVar()
# var.set(False)  # Set the initial state to False (off)
#
# # Create the toggle (Checkbutton)
# toggle = ttk.Checkbutton(window, text="Global", variable=var, command=toggle_global)
# toggle.pack(pady=10)
#
# # Create radio buttons for each option
# options = ["Off", "TriggerBot", "Soft Aim", "AIMBOT (unsafe if your teammates are spectating)"]
# selected_option = tk.StringVar()
# selected_option.set(options[0])  # Set the initial option
#
# option_frame = tk.Frame(window)
# option_frame.pack(pady=10)
#
# radio_buttons = []
# for option in options:
#     radio_button = ttk.Radiobutton(option_frame, text=option, variable=selected_option, value=option, command=update_selection)
#     radio_button.pack(anchor=tk.W)  # Use anchor=tk.W to align to the left
#     radio_buttons.append(radio_button)
#
# # Add a slider for "Soft Aim" strength
# soft_aim_frame = tk.Frame(window)
# soft_aim_frame.pack(pady=10)
#
# soft_aim_label = tk.Label(soft_aim_frame, text="Soft Aim Strength:")
# soft_aim_label.pack(side=tk.LEFT)
#
# strength_value_label = tk.Label(soft_aim_frame, text=0)
# strength_value_label.pack(side=tk.RIGHT)
# strength_value_label.config(state=tk.DISABLED)
#
# strength_scale = ttk.Scale(soft_aim_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=150, command=update_strength_scale)
# strength_scale.pack(side=tk.RIGHT)
# strength_scale.set(50)  # Set initial strength value
# strength_scale.config(state=tk.DISABLED)
#
#
#
# toggle_global()  # Call initially to set the state based on the initial value of 'var'
#
# # Create a label to display the selected option
# # label = tk.Label(window, text="Selected option: off")
# # label.pack(pady=10)
#
# # Run the Tkinter event loop
# sv_ttk.set_theme("dark")
# # window.configure(background='black')
# window.mainloop()
# import time
#
# from SettingsUI import SettingsUI
#
# settingsUi = SettingsUI()
# time.sleep(1)
# while True:
#     print(settingsUi.strengthValue)





# import time
# import torch
#
# import numpy as np
# import cv2
# from mss import mss
# from PIL import Image
#
# bounding_box = {'top': 340, 'left': 800, 'width': 350, 'height': 400}
#
#
# dummy_frame = torch.randn(1,3,416,736).cuda() #dummy data
#
# device = torch.device("cuda")
# model = torch.hub.load(r'C:\proj\pypy\val-cheat\yolov5', 'custom', path=r'C:\proj\pypy\val-cheat\best.pt', source='local').to(device)
#
# model.conf = 0.40
# model.maxdet = 10
# model.apm = True
# model.eval()
# model.cuda()
#
# sct = mss()
# start = time.time()
# for i in range(10):
#     screenshot = np.array(sct.grab(bounding_box))
#     out = model(screenshot, size=736).pandas().xyxy[0]
# time_spent = time.time() - start
# fps = 10*32 / time_spent   # batches * batch_size
# print(f"{fps:.2f} fps") # 344 FPS on T4 in colab




# sct = mss()
# start_time = time.time()
# counter = 0
#
# while True:
#     counter += 1
#     if (time.time() - start_time) > 1:
#         fps = "fps:" + str(int(counter / (time.time() - start_time)))
#         print(fps)
#         counter = 0
#         start_time = time.time()
#
#
#     sct_img = sct.grab(bounding_box)
#     scr_img = np.array(sct_img)
#
#     # cv2.imshow('screen', scr_img) # display screen in box
#     scr_img = model(scr_img, size=736).pandas().xyxy[0]
#     # cv2.imshow('Testing', scr_img)
#
#     # if (cv2.waitKey(1) & 0xFF) == ord('q'):
#     #     cv2.destroyAllWindows()
#     #     break



import math

fishes = [3, 4, 3, 1, 2]

numDays = 400
totalFish = 0
for fish in fishes:
    totalFish += math.pow(2, int((numDays - fish - 1) / 7) + 1)
print(f"total fish {totalFish}")
print(totalFish == 720575940379279360)


print(fishes)
print(len(fishes))
# print(totalFish)

print(math.pow(2, 57) * 5)






# def poisson(jour, horloge):
#     exponent = 0
#     jour = jour - horloge
#     exponent = exponent + 1
#     while jour - 7 > 0:
#         jour = jour - 7
#         exponent = exponent + 1
#     print(exponent)
#     return math.pow(2, exponent)
#
# total_fish = 0
# for i in fishes:
#     total_fish = total_fish + poisson(9, i)
# print(total_fish)
