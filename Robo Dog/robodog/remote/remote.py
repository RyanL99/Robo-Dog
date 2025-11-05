import time

def Remote(cfg,qs):
    mq=qs['motion']; t=0
    while True:
        mq.put({'type':'HB','t':t}); t+=0.1; time.sleep(0.5)
