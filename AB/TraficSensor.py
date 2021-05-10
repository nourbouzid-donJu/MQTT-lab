import struct
import time
import csv
import os
import Publish

rootDir = os.path.dirname(__file__)

def main():
    client = Publish.open_connection("A_B_Trafic")
    while True: 
        with open('{}/h1.csv'.format(rootDir), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            lineCount = 0
            for row in spamreader:
                if lineCount == 0:
                    lineCount +=1
                    #print(row[16])
                else:
                    trafic = float(row[16])
                    traficLoad = struct.pack('f',trafic)
                    Publish.publish_data(traficLoad,"sensor/AB/trafic", client) # publish the trafic 
                    print("Trafic: " + str(trafic))
                    time.sleep(1)
            

    Publish.close_connection()



