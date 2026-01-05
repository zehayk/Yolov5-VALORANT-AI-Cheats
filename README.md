# Yolov5-VALORANT-AI-Cheats
Demo 1:

[![Demo 1](https://img.youtube.com/vi/as775sPdsms/0.jpg)](https://www.youtube.com/watch?v=as775sPdsms)


Inspired by pyturtle: https://github.com/pyturtle/Valorant-AI-cheats

## Detection
Valorant cheats created by using Yolov5 to train computer vision model to detect purple enemies. Used NVIDIA Cuda for optimization, and more optimization will be added in the future.

## Mouse spoofing
To bypass Valorant's restrictions on second mouses and mouse movement libraries, I've used an Arduino Leonardo connected to the PC to emulate mouse. The Arduino receives mouse movement data via Serial through Python code. Additionally, I used USB Host Shield on the Arduino to connect my physical mouse, and the HID Mouse Reporter library is used to transmit its inputs to PC.
