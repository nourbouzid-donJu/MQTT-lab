import _thread
import MQTT
import HTTP

try: 
   _thread.start_new_thread(MQTT.main, ())
   _thread.start_new_thread(HTTP.main, ())
except KeyboardInterrupt:
   print("KEy")
except:
   print ("Error: unable to start thread")

try: 
    while 1:
       pass
except KeyboardInterrupt:
    quit()