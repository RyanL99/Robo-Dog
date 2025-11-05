
try:
    import board, busio
    from adafruit_pca9685 import PCA9685
    from adafruit_motor import servo as ada
except: board=None

class ServoHub:
    def __init__(self, boards):
        if board is None: raise RuntimeError("Install adafruit-circuitpython libs")
        self.i2c=busio.I2C(board.SCL,board.SDA)
        self.p=[]
        for b in boards:
            p=PCA9685(self.i2c,address=int(b["address"],16)); p.frequency=b["frequency"]; self.p.append(p)
        self.cache={}
    def servo(self,d,ch,mi,ma):
        k=(d,ch,mi,ma)
        if k in self.cache: return self.cache[k]
        s=ada.Servo(self.p[d].channels[ch],min_pulse=mi,max_pulse=ma)
        self.cache[k]=s
        return s
    def close(self):
        for p in self.p:
            try: p.deinit()
            except: pass
