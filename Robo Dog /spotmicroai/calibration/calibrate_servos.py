
import sys, time, tty, termios
from spotmicroai.utilities.config import load_config, save_config
from spotmicroai.utilities.servo_driver import ServoBank

L="\x1b[D"; R="\x1b[C"; D="\x1b[B"; U="\x1b[A"

def getch():
    fd=sys.stdin.fileno(); old=termios.tcgetattr(fd)
    try:
        tty.setraw(fd); c=sys.stdin.read(1)
        if c=="\x1b": return c+sys.stdin.read(2)
        return c
    finally: termios.tcsetattr(fd,termios.TCSADRAIN,old)

def main():
    cfg=load_config(); joints=cfg["joints"]
    bank=ServoBank(cfg["pca9685"])
    ang=[j["rest_deg"] for j in joints]
    sv=[bank.get(j["driver"],j["channel"],j["min_us"],j["max_us"]) for j in joints]

    def apply(i):
        j=joints[i]; sv[i].angle=max(j["min_deg"],min(j["max_deg"],ang[i]))
    for i in range(len(joints)): apply(i)
    print("j/J select • arrows move • s save • q quit")

    i=0
    while True:
        print(f"\r{i+1}: {joints[i]['name']} {ang[i]:.1f}°",end="")
        c=getch()
        if c=="q": break
        if c=="j": i=(i-1)%len(joints)
        if c=="J": i=(i+1)%len(joints)
        if c==L: ang[i]-=1
        if c==R: ang[i]+=1
        if c==D: ang[i]-=5
        if c==U: ang[i]+=5
        if c=="s":
            joints[i]["rest_deg"]=round(ang[i],2); save_config(cfg)
        apply(i)
    bank.close()

if __name__=="__main__": main()
