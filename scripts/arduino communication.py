import serial
from threading import Thread
import time
arduino = serial.Serial(port='COM10', baudrate=9600)
#
# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data
#
# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value


# arduino.write(b's')
arduino.write(b'coords:')
# arduino.close()


def readSerial():
    while True:
        # print("#read#")
        print(arduino.readline().decode())

Thread(target=readSerial, args=()).start()


while True:  # test message : "coords:123,123!"
    a = input("Enter message: ")
    arduino.write(a.encode())

