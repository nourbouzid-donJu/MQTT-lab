# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import csv
import os

hostName = "10.0.2.10"
serverPort = 8080

locationArray = ["AB", "BC", "CD"]

rootDir = os.path.dirname(__file__)

#-------------------------------------------------#

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        content = "<p>AB({})</p><p>BC({})</p><p>CD({})</p>"
        content = content.format(get_data(0),get_data(1),get_data(2))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://LatestDroneData</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(content, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


def get_data(location):
    #get data from csv file
    #set default values, (drone doesn't fly with this values)
    temp = 0.0
    windSpeed = 4.0
    windDir = "S"
    trafic = 10.0
    with open('{}/{}_sensor_data.csv'.format(rootDir, locationArray[location]), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            lineCount = 0
            for row in spamreader:
                if lineCount == 0:
                    lineCount +=1
                else:
                   if row[0] != "null":
                    temp = float(row[0])
                   if row[1] != "null":
                    windSpeed = float(row[1])
                   if row[2] != "null":
                    windDir = row[2]
                   if row[3] != "null":
                    trafic = float(row[3])
    data = "temp:{},windSpeed:{},windDir:{},trafic:{}"
    return data.format(str(temp),str(windSpeed),windDir,str(trafic))

#-------------------------------------------------#

def main():    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    return
