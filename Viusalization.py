# This Script is purely for visualization purposes
# WIth this script the flying drone is visualized (as in the Video in the Lab)
# We didn't integrate this in the Lab because we had problems to integrate it in core and it took to much time

# move an Image on the canvas with tkinter
import os
import tkinter as tk
import paho.mqtt.client as mqtt 
from time import sleep


root = tk.Tk()
rootDir = os.path.dirname(__file__)


canvas = tk.Canvas(root, width=1678, height=726)
canvas.pack() 

cityimg = tk.PhotoImage(file="/home/ilab/Desktop/RomeoAndJuliet/Pictures/cityFinal.png")
city = canvas.create_image(0, 0, anchor=tk.NW, image=cityimg)
img = tk.PhotoImage(file="/home/ilab/Desktop/RomeoAndJuliet/Pictures/smallDrone.png")
image = canvas.create_image(238, 280, anchor=tk.NW, image=img)
 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("display")

def on_message(client, userdata, msg):
    print(msg.payload)
    if msg.payload.decode('utf-8') == "DroneAB":
        for x in range(140):
            canvas.move(image, 3, -2)
            sleep(0.05)
    if msg.payload.decode('utf-8') == "DroneBC":
        for x in range(200):
            canvas.move(image, 2, 1)
            sleep(0.035)
    if msg.payload.decode('utf-8') == "DroneCD":
        for x in range(85):
            canvas.move(image, 3, 0)
            sleep(0.05)
# Connects to Broker and subscribes to topic
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

client.loop_start()

root.mainloop()