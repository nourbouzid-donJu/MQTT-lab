import Publish
import struct
import time
import csv
import os

rootDir = os.path.dirname(__file__)

def findWindDir(degree): #taransalte deg to wind direction
    degRoundInt = ((round((int(degree))/90))%4)
    if degRoundInt == 0:
        return "N"
    if degRoundInt == 1:
       return "O"
    if degRoundInt == 2:
        return "S"
    if degRoundInt == 3:
        return "W"

def main():
    client = Publish.open_connection("A_B_Wind")
    while True: 
        with open('{}/h1.csv'.format(rootDir), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            lineCount = 0
            for row in spamreader:
                if lineCount == 0:
                    lineCount +=1
                    #print(row[6])
                    #print(row[7])
                else:
                    direction = int(float(row[6]))
                    speed = float(row[7])
                    strWindDir = findWindDir(direction)
                    speedLoad = struct.pack('f',speed)
                    print("WindSpeed: " + str(speed))
                    Publish.publish_data(speedLoad,"sensor/AB/WindSpeed", client) # publish wind speed
                    print("WindDir: " + strWindDir)
                    #print(direction)
                    Publish.publish_data(strWindDir,"sensor/AB/WindDir", client) # publish wind wirection
                    time.sleep(2)
            

    Publish.close_connection()



