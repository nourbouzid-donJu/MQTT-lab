import time
import requests
import paho.mqtt.client as mqtt
import re
import Visualization2


def open_connection(): #connect to MQTT broker
    client.connect("10.0.5.10", 1883, 60)
    client.loop_start()

def close_connection(): #disconnect from MQTT broker
    client.loop_stop()
    client.disconnect()

# Sends an HTTP request to the IoT Platform
def get_data():
    data = requests.get('http://10.0.2.10:8080')
    if (data.status_code == 200):
        print("HTTP request worked")
        #print(data.text)
        return data.text
    else:
        print("HTTP request did not work!")
        return None

# Formats the data of the HTTP request
def format_data(data_no_format, current_section):
    data_section_array = ["AB", "BC", "CD"]
    section_data = data_no_format.split(data_section_array[current_section], 1)[1]
    try:    
        temp_string = re.search('temp:(.+?),', section_data).group(1)
        wind_speed_data = re.search('windSpeed:(.+?),', section_data).group(1)
        wind_dir_data = re.search('windDir:(.+?),', section_data).group(1)
        trafic_string = re.search('trafic:(.+?)\)', section_data).group(1)
        print(temp_string + "\n" + wind_speed_data + "\n" + wind_dir_data + "\n" + trafic_string)
    except AttributeError:
        print("Attribute Error")
    return float(temp_string), float(wind_speed_data), wind_dir_data, float(trafic_string)

# Evaluates the sensor data
def evaluate_data(temp, wind_speed, wind_dir, trafic):
    all_sensor_data = temp != "null" and wind_speed != "null" and wind_dir != "null" and trafic != "null"
    good_flight_conditions = temp < 25.0 and temp > 12.0 and wind_speed < 3.0 and wind_dir != "S" and trafic < 6
    if all_sensor_data and good_flight_conditions:
       drone_status = "fly"
    else:
       drone_status = "stop"
    return drone_status 

# Main drone method
def start_drone():
    current_section = 0
    section_array = ["DroneAB", "DroneBC", "DroneCD", "Juliet"]
    print("Start up drone")
    try:
        while(section_array[current_section] != "Juliet"):
            data_no_format = get_data()
            if (not(data_no_format is None)):
                temp_data, wind_speed_data, wind_dir_data, trafic = format_data(data_no_format, current_section)
                if (evaluate_data(temp_data, wind_speed_data, wind_dir_data, trafic) == "fly"):
                    print("Drone starts from " + section_array[current_section])
                    m = client.publish("display", section_array[current_section])
                    m.wait_for_publish()
                    time.sleep(3)
                    current_section = current_section + 1
                    section = section_array[current_section]
                    print("Drone lands at " + section)
                else:
                    print("Drone does not start from " + section_array[current_section])
            time.sleep(5)
    
        m = client.publish(Visualization2.c1, Visualization2.c2)
        m.wait_for_publish()
        print("Congrats! Your letter reached Juliet!")
    except KeyboardInterrupt:
        pass

#-------------------------------------------------#

client = mqtt.Client(client_id="Drone_temp")
open_connection()
start_drone()
close_connection()

