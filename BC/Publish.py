import paho.mqtt.client as paho

def publish_data(data,topic, client): #publish mqtt data
    m = client.publish(topic, payload=data,qos=0, retain=False)
    #print("publish now")
    m.wait_for_publish()
    #print("publish done")

def open_connection(clientID): #connect to MQTT broker
    client = paho.Client(client_id=clientID)
    client.connect("10.0.5.10", 1883, 60)
    client.loop_start()
    return client

def close_connection(): #disconnect from MQTT broker
    client.loop_stop()
    client.disconnect()

