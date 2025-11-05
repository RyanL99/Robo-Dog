
from typing import Dict, Any, List
try:
    import board, busio
    from adafruit_pca9685 import PCA9685
    from adafruit_motor import servo as ada_servo
except:
    board = busio = PCA9685 = ada_servo = None

class ServoBank:
    def __init__(self, pca_list: List[Dict[str, Any]]):
        if board is None: raise RuntimeError("Adafruit libs missing")
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pcas = []
        for e in pca_list:
            pca = PCA9685(self.i2c, address=int(e["address"],16)); pca.frequency=e["frequency"]; self.pcas.append(pca)
        self.s = {}

    def get(self, d, ch, mi, ma):
        key=(d,ch,mi,ma)
        if key in self.s: return self.s[key]
        s=ada_servo.Servo(self.pcas[d].channels[ch],min_pulse=mi,max_pulse=ma)
        self.s[key]=s; return s

    def close(self):
        for p in self.pcas:
            try: p.deinit()
            except: pass
