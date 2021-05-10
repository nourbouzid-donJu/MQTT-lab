import _thread
import TempSensor
import WindDrone
import TraficSensor

try: 
   _thread.start_new_thread(TempSensor.main, ())
   _thread.start_new_thread(WindDrone.main, ())
   _thread.start_new_thread(TraficSensor.main, ())

except:
   print ("Error: unable to start thread")
   quit()

try: 
    while 1:
       pass
except KeyboardInterrupt:
    quit()