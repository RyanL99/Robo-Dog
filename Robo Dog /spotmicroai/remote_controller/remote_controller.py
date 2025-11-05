
import time
def RemoteControllerController(cfg, channels):
    mq = channels["motion"]; t=0
    while True:
        try: mq.put({"type":"HB","t":t})
        except: pass
        t+=0.1; time.sleep(0.5)
