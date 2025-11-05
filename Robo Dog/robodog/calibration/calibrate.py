
import sys,tty,termios,time
from robodog.util.config import load,save
from robodog.util.servo import ServoHub

L="\x1b[D";R="\x1b[C";D="\x1b[B";U="\x1b[A"
def key():
    fd=sys.stdin.fileno(); old=termios.tcgetattr(fd)
    try:
        tty.setraw(fd); c=sys.stdin.read(1)
        if c=="\x1b": return c+sys.stdin.read(2)
        return c
    finally: termios.tcsetattr(fd,termios.TCSADRAIN,old)

def main():
    cfg=load(); js=cfg["joints"]; hub=ServoHub(cfg["pca9685"])
    ang=[j["rest_deg"] for j in js]
    sv=[hub.servo(j["driver"],j["channel"],j["min_us"],j["max_us"]) for j in js]
    def apply(i):
        j=js[i]; sv[i].angle=max(j["min_deg"],min(j["max_deg"],ang[i]))
    for i in range(len(js)): apply(i)
    print("j/J arrows s save q quit")
    i=0
    while True:
        print(f"\r{i+1}: {js[i]['name']} {ang[i]:.1f}",end="")
        c=key()
        if c=="q": break
        if c=="j": i=(i-1)%len(js)
        if c=="J": i=(i+1)%len(js)
        if c==L: ang[i]-=1
        if c==R: ang[i]+=1
        if c==D: ang[i]-=5
        if c==U: ang[i]+=5
        if c=="s":
            js[i]["rest_deg"]=round(ang[i],2); save(cfg)
        apply(i)
    hub.close()

if __name__=="__main__": main()
