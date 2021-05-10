import paho.mqtt.client as paho

def publish_data(data,topic, client): #publish mqtt data
    m = #TODO
    #print("publish now")
    m.wait_for_publish()
    #print("publish done")

def open_connection(clientID): #connect to MQTT broker
    client = #TODO
    client.connect("", 1883, 60)#TODO set the IP
    client.loop_start()
    return client

def close_connection(): #disconnect from MQTT broker
    client.loop_stop()
    client.disconnect()

