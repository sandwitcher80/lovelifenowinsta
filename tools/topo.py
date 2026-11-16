import numpy as np, contourpy, sys, json
rng=np.random.default_rng(7)
def waves(n,lmin,lmax,seed):
    r=np.random.default_rng(seed)
    out=[]
    for _ in range(n):
        lam=r.uniform(lmin,lmax); th=r.uniform(0,2*np.pi)
        out.append((2*np.pi/lam*np.cos(th),2*np.pi/lam*np.sin(th),r.uniform(0,2*np.pi),lam))
    return out
BASE=waves(46,160,950,11)
WARP=waves(10,500,1400,5)
def field(X,Y):
    wx=np.zeros_like(X);wy=np.zeros_like(X)
    for kx,ky,ph,lam in WARP:
        wx+=np.sin(kx*X+ky*Y+ph)*60
        wy+=np.cos(kx*X+ky*Y+ph*1.3)*60
    Xw=X+wx/ 3.2; Yw=Y+wy/3.2
    z=np.zeros_like(X)
    for kx,ky,ph,lam in BASE:
        z+=np.sin(kx*Xw+ky*Yw+ph)*(lam/950)**1.0
    return z/3.1
def slide_paths(i,W=1080,H=1350,step=6,levels=17):
    xs=np.arange(-20,W+21,step)+i*W  # global x continues across slides
    ys=np.arange(-20,H+21,step)
    X,Y=np.meshgrid(xs.astype(float),ys.astype(float))
    z=field(X,Y)
    # fixed global levels so slides match
    lv=np.linspace(-2.5,2.5,levels)+0.0
    g=contourpy.contour_generator(xs-i*W,ys,z)
    strong=[];soft=[]
    for k,l in enumerate(lv):
        for line in g.lines(l):
            if len(line)<8: continue
            p=line[::3] if len(line)>60 else (line[::2] if len(line)>30 else line)
            d="M%.1f %.1f"%tuple(p[0])
            for a,b in zip(p[:-1],p[1:]):
                m=(a+b)/2
                d+="Q%.1f %.1f %.1f %.1f"%(a[0],a[1],m[0],m[1])
            (soft if k%3==2 else strong).append(d)
    return "".join(strong),"".join(soft)
if __name__=="__main__":
    for i in range(6):
        s,f=slide_paths(i)
        print(i,len(s)+len(f))
