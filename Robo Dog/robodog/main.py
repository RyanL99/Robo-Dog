
import time,signal,sys,logging,multiprocessing as mp
from robodog.util.config import load
from robodog.util.queues import make
from robodog.motion.motion import Motion
from robodog.remote.remote import Remote

def spawn(fn,name,*a):
    p=mp.Process(target=fn,name=name,args=a,daemon=True); p.start(); return p

def main():
    logging.basicConfig(level=logging.INFO)
    cfg=load()
    qs=make(["motion","remote"])
    ps=[spawn(Motion,"Motion",cfg,qs), spawn(Remote,"Remote",cfg,qs)]
    def stop(*_):
        for q in qs.values():
            try:q.put({"type":"STOP"})
            except: pass
        time.sleep(0.2)
        for p in ps:
            if p.is_alive(): p.terminate()
        sys.exit(0)
    signal.signal(signal.SIGINT,stop); signal.signal(signal.SIGTERM,stop)
    logging.info("RoboDog runtime running — integrate gait & joystick next.")
    while True: time.sleep(1)

if __name__=="__main__": main()
