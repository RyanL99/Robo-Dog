def Motion(cfg,qs):
    q=qs['motion']
    while True:
        try: q.get(timeout=0.1)
        except: pass
