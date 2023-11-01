import tkinter
import tkinter as tk
from tkinter import ttk
import sv_ttk
import threading


class SettingsUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def setRadioButtons(self):
        self.options = ["Off", "TriggerBot", "Soft Aim", "AIMBOT (unsafe if your teammates are spectating)"]
        self.selected_option = tk.StringVar()
        self.selected_option.set(self.options[0])  # Set the initial option

        option_frame = tk.Frame(self.window)
        option_frame.pack(pady=10)

        self.radio_buttons = []
        for option in self.options:
            radio_button = ttk.Radiobutton(option_frame, text=option, variable=self.selected_option, value=option,
                                           command=self.update_selection)
            radio_button.pack(anchor=tk.W)  # Use anchor=tk.W to align to the left
            self.radio_buttons.append(radio_button)

    def setSoftAimScale(self):
        soft_aim_frame = tk.Frame(self.window)
        soft_aim_frame.pack(pady=10)

        soft_aim_label = tk.Label(soft_aim_frame, text="Soft Aim Strength:")
        soft_aim_label.pack(side=tk.LEFT)

        self.strength_value_label = tk.Label(soft_aim_frame, text=0)
        self.strength_value_label.pack(side=tk.RIGHT)
        self.strength_value_label.config(state=tk.DISABLED)

        strength_scale = ttk.Scale(soft_aim_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=150,
                                   command=self.update_strength_scale)
        strength_scale.pack(side=tk.RIGHT)
        strength_scale.set(self.strengthValue)  # Set initial strength value
        strength_scale.config(state=tk.DISABLED)

        self.softAimComponents.append(soft_aim_label)
        self.softAimComponents.append(self.strength_value_label)
        self.softAimComponents.append(strength_scale)

    def toggleSoftAimComponents(self, mode):
        for component in self.softAimComponents:
            component.config(state=mode)

    def update_selection(self):
        selection = self.selected_option.get()
        # label.config(text=f"Selected option: {selection}")
        if selection == self.options[2]:
            self.toggleSoftAimComponents(tkinter.NORMAL)
        else:
            self.toggleSoftAimComponents(tkinter.DISABLED)

    def update_strength_scale(self, value):
        self.strengthValue = int(float(value))
        self.strength_value_label.config(text=self.strengthValue)

    def toggle_global(self):
        if self.isGlobalOn():  # If Global is selected
            for radio_button in self.radio_buttons:
                radio_button.config(state=tk.NORMAL)

            if self.selected_option.get() == self.options[2]:
                self.toggleSoftAimComponents(tk.NORMAL)
        else:
            for radio_button in self.radio_buttons:
                radio_button.config(state=tk.DISABLED)
            self.toggleSoftAimComponents(tk.DISABLED)

    def callback(self):
        self.window.quit()

    def isGlobalOn(self):
        return self.var.get()

    def run(self):
        # Create window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.callback)
        self.window.title("Toggle and Options")
        self.window.geometry("400x300")

        # Create components holders
        self.softAimComponents = []
        self.strength_value_label = None
        self.options = []
        self.selected_option = None
        self.radio_buttons = []
        self.strengthValue = 50

        # Create the toggle button
        self.var = tk.BooleanVar()
        self.var.set(False)
        self.toggle = ttk.Checkbutton(self.window, text="Global", variable=self.var, command=self.toggle_global)
        self.toggle.pack(pady=10)

        # Call create components functions
        self.setRadioButtons()
        self.setSoftAimScale()

        # Call toggle for first time
        self.toggle_global()

        print("Started!")
        sv_ttk.set_theme("dark")
        self.window.mainloop()

