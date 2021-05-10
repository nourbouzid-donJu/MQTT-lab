import paho.mqtt.client as mqtt #https://pypi.org/project/paho-mqtt/#multiple
import struct #https://docs.python.org/3.1/library/struct.html
import csv
import os

#-------------------------------------------------#

#gloabl variables
locationArray = ["AB", "BC", "CD"]
drone_location = ["DroneAB", "DroneBC", "DroneCD"]

rootDir = os.path.dirname(__file__)
#-------------------------------------------------#

def csv_file_init():
    #initialize csv File, deletes everything, sets header
    location = 0
    while location < 3:
        path = '{}/{}_sensor_data.csv'.format(rootDir, locationArray[location])
        #TODO initialize all csv files (path already calculated)
        #at the end the file should only consist of the line "Temp,WindSpeed,WindDir,trafic"
        location = location + 1

def find_location(topic):
    topic_array = topic.split("/")
    if topic_array[1] == "AB":
       return 0
    elif topic_array[1] == "BC":
       return 1
    elif topic_array[1] == "CD":
       return 2
    else:
       return -1


def write_csv(location, temperature, speed, windDir, trafic):
    if location > -1:
       path = '{}/{}_sensor_data.csv'.format(rootDir, locationArray[location])
        #TODO add the data (temperature, speed, windDir, trafic) in the right csv file (path already calculated)
    else:
       print("Ops, this was a wrong topic! Topic: " + msg.topic)

#-------------------------------------------------#
#on_message
def on_message_temp(client, userdata, msg):
    #print(msg.topic + " TEMP " + str(msg.payload))

    fmt = 'f'
    tupel = struct.unpack(fmt, msg.payload)
    #print(tupel)
    #check if the transfer was correct
    if struct.calcsize(fmt) == len(msg.payload):
        temperature = tupel[0]
    else: 
        print("Something went wrong with the unpacking!")   

    print(msg.topic + " TEMP " + str(temperature))
    location = find_location(msg.topic)
 
    write_csv(location, temperature, 'null', 'null', 'null')


def on_message_windSpeed(client, userdata, msg):
    #print(msg.topic + " Speed " + str(msg.payload))

    fmt = 'f'
    tupel = struct.unpack(fmt, msg.payload)
    #print(tupel)
    #check if the transfer was correct
    if struct.calcsize(fmt) == len(msg.payload):
        speed = tupel[0]
    else:
        print("Something went wrong with the unpacking!")

    print(msg.topic + " Speed " + str(speed))
    location = find_location(msg.topic)
 
    write_csv(location, 'null', speed, 'null', 'null')
    

def on_message_windDir(client, userdata, msg):
    #print(msg.topic + " Dir " + str(msg.payload))

    location = find_location(msg.topic)
    windDir = msg.payload.decode('utf-8')
 
    print(msg.topic + " DIR " + windDir)
    write_csv(location, 'null', 'null', windDir, 'null')

def on_message_trafic(client, userdata, msg):
    #print(msg.topic + " Trafic " + str(msg.payload))

    fmt = 'f'
    tupel = struct.unpack(fmt, msg.payload)
    #print(tupel)
    #check if the transfer was correct
    if struct.calcsize(fmt) == len(msg.payload):
        trafic = tupel[0]
    else: 
        print("Something went wrong with the unpacking!")   

    print(msg.topic + " Trafic " + str(trafic))
    location = find_location(msg.topic)
 
    write_csv(location, 'null', 'null', 'null', trafic)
       
def on_message(client, userdata, msg):
    print("The topic of this sensor isn't covered! " + msg.topic)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

#-------------------------------------------------#
def main():

    csv_file_init()

    #initialize client
    global client
    client = mqtt.Client("IoT")

    client.message_callback_add("sensor/+/temp", on_message_windSpeed)
    client.message_callback_add("sensor/+/WindSpeed", on_message_trafic)
    client.message_callback_add("sensor/+/WindDir", on_message_windDir)
    client.message_callback_add("sensor/+/trafic", on_message_temp)
    client.on_message = on_message

    client.on_connect = on_connect

    #client.on_publish = on_publish
    #client.on_log = on_log
    client.connect("10.0.5.10", 1883, 60) #(broker, port, timeout in seconds) 10.0.5.10

    #subscribe
    client.subscribe("sensor/#") #listens on sensor data

    client.loop_forever()
    


