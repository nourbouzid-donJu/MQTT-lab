import struct
import time
import csv
import os
import Publish

rootDir = os.path.dirname(__file__)

def main():
    client = Publish.open_connection("A_B_temp")
    while True: 
        with open('{}/h1.csv'.format(rootDir), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            lineCount = 0
            for row in spamreader:
                if lineCount == 0:
                    lineCount +=1
                    #print(row[4])
                else:
                    #print("TEST")
                    #print(row[4])
                    temp = float(row[4])
                    tempLoad = struct.pack('f',temp)
                    Publish.publish_data(tempLoad,"sensor/AB/temp", client) # publish the temperature 
                    print("Temp: " + str(temp))
                    time.sleep(3)
            

    Publish.close_connection()



