
def MotionController(cfg, channels):
    q = channels["motion"]
    while True:
        try: msg=q.get(timeout=0.1)
        except: msg=None
