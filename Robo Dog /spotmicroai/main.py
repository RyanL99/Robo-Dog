
import time, signal, sys, logging, multiprocessing as mp
from spotmicroai.utilities.config import load_config
from spotmicroai.utilities import queues as q
from spotmicroai.motion_controller.motion_controller import MotionController
from spotmicroai.remote_controller.remote_controller import RemoteControllerController

def spawn(fn, name, *args):
    p = mp.Process(target=fn, name=name, args=args, daemon=True); p.start(); return p

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    cfg = load_config()
    channels = q.get_queues(["motion","remote"])
    procs=[spawn(MotionController,"Motion",cfg,channels),
           spawn(RemoteControllerController,"Remote",cfg,channels)]

    def stop(*_):
        for qv in channels.values():
            try: qv.put({"type":"STOP"}); 
            except: pass
        time.sleep(0.2)
        for p in procs:
            if p.is_alive(): p.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT,stop); signal.signal(signal.SIGTERM,stop)
    logging.info("Started runtime. Replace motion/remote with real code.")
    while True: time.sleep(1)

if __name__=="__main__": main()
