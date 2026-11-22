"""Rendert ein Reel (1080x1920, 30fps, stumm) aus einer JSON-Spec, ohne Video-KI (Code-Frames + ffmpeg).
Nutzung: python3 tools/reel.py specs/reel-<name>.json   -> reels/<name>/reel.mp4 + cover.png
Spec: {"name","start","scenes":[...]}
Szenen: {"type":"text","text":"...","accent":"Wort in Serif-Kursiv","secs":3,"pal":"BL"|"BS"|"NV"}
        {"type":"breath","in":4,"out":6,"cycles":3,"pal":"BL"}  (Kreis waechst beim Einatmen, schrumpft beim Ausatmen, mit Zaehler)
        {"type":"end","text":"...","pal":"BS"}  (letzte Karte mit @jens.lovelifenow)
Hinweis: Musik kann in Instagram beim Veroeffentlichen/ueber Metricool nicht per API gesetzt werden (nur Audio-Katalog), Reel laeuft stumm bzw. Jens ergaenzt Ton in der App."""
import sys, json, math, subprocess, pathlib, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from topo import slide_paths
from playwright.sync_api import sync_playwright
W,H,FPS=1080,1920,30
PAL=dict(BL=dict(bg="#2D5AAA",fg="#FFFFFF",ac="#F8EEE8",c1="rgba(255,255,255,0.28)",c2="rgba(255,255,255,0.14)"),
         BS=dict(bg="#F8EEE8",fg="#2D5AAA",ac="#2D5AAA",c1="#FFFFFF",c2="rgba(255,255,255,0.6)"),
         NV=dict(bg="#1B3470",fg="#FFFFFF",ac="#DCE6F5",c1="rgba(220,230,245,0.30)",c2="rgba(220,230,245,0.14)"))
def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
FB='/usr/share/fonts/opentype/inter/Inter-Bold.otf'; FR='/usr/share/fonts/opentype/inter/Inter-Regular.otf'
FS='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'
def font(p,s): return ImageFont.truetype(p,s)
spec=json.load(open(sys.argv[1])); OUT=ROOT/'reels'/spec['name']; OUT.mkdir(parents=True,exist_ok=True)
# Hintergruende
bgs={}
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']); pg=br.new_page(viewport={'width':W,'height':H})
    for k,(name,p) in enumerate(PAL.items()):
        s,f=slide_paths(spec.get('start',78)+k,W=W,H=H)
        svg=f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" fill="none" stroke-width="3" stroke-linecap="round"><path stroke="{p["c1"]}" d="{s}"/><path stroke="{p["c2"]}" d="{f}"/></svg>'
        pg.set_content(f'<body style="margin:0;background:{p["bg"]}">{svg}</body>'); pg.wait_for_timeout(150)
        bgs[name]=Image.open(io.BytesIO(pg.screenshot(clip={'x':0,'y':0,'width':W,'height':H}))).convert('RGB')
    br.close()
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def ease(t): return 0.5-0.5*math.cos(math.pi*min(max(t,0),1))
def draw_text(img,text,accent,fs,cx,cy,color,alpha,acolor=None):
    ov=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(ov); f=font(FB,fs); fa=font(FS,fs)
    lines=wrap(d,text,f,W-200); lh=int(fs*1.18); y=cy-len(lines)*lh//2
    for ln in lines:
        # Akzentwort in Serif-Kursiv
        parts=[]; 
        if accent and accent in ln:
            a,b=ln.split(accent,1); parts=[(a,f),(accent,fa),(b,f)]
        else: parts=[(ln,f)]
        tw=sum(d.textlength(t,font=ft) for t,ft in parts); x=cx-tw/2
        for t,ft in parts:
            d.text((x,y),t,font=ft,fill=hexc(acolor if (ft is fa and acolor) else color)+(int(255*alpha),)); x+=d.textlength(t,font=ft)
        y+=lh
    img.paste(Image.alpha_composite(img.convert('RGBA'),ov).convert('RGB'))
def frames():
    for sc in spec['scenes']:
        p=PAL[sc.get('pal','BL')]; bg=bgs[sc.get('pal','BL')]
        if sc['type']=='text' or sc['type']=='end':
            n=int(sc.get('secs',3)*FPS) if sc['type']=='text' else int(sc.get('secs',3.5)*FPS)
            for i in range(n):
                t=i/FPS; T=n/FPS; a=min(ease(t/0.4),ease((T-t)/0.35)) if sc['type']=='text' else ease(t/0.4)
                im=bg.copy(); 
                fs=sc.get('fs',96)
                draw_text(im,sc['text'],sc.get('accent'),fs,W//2,H//2-40,p['fg'],a,p['ac'])
                if sc['type']=='end':
                    d=ImageDraw.Draw(im); f=font(FS,40); tx='@jens.lovelifenow'; tw=d.textlength(tx,font=f)
                    bx0,by0=W//2-tw/2-48,H//2+360; d.rectangle([bx0,by0,bx0+tw+96,by0+112],fill=(255,255,255),outline=hexc(p['fg']),width=3); d.text((bx0+48,by0+30),tx,font=f,fill=hexc('#2D5AAA'))
                yield im
        elif sc['type']=='breath':
            for c in range(sc.get('cycles',3)):
                for phase,secs in (('in',sc['in']),('out',sc['out'])):
                    n=int(secs*FPS)
                    for i in range(n):
                        t=i/n; k=ease(t) if phase=='in' else 1-ease(t)
                        r=int(190+210*k); im=bg.copy(); ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
                        cx,cy=W//2,H//2-60
                        d.ellipse([cx-r-40,cy-r-40,cx+r+40,cy+r+40],fill=hexc(p['ac'])+(40,))
                        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=hexc(p['ac'])+(int(70+60*k),),outline=hexc(p['fg'])+(200,),width=4)
                        im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
                        sec=int(i/FPS)+1
                        label='Einatmen' if phase=='in' else 'Ausatmen'
                        draw_text(im,label,None,84,W//2,cy-r-130,p['fg'],1.0)
                        draw_text(im,str(min(sec,secs)),None,200,W//2,cy,p['fg'],1.0)
                        draw_text(im,f"Runde {c+1} von {sc.get('cycles',3)}",None,40,W//2,H-250,p['ac'],1.0)
                        yield im
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(OUT/'reel.mp4')]
pr=subprocess.Popen(cmd,stdin=subprocess.PIPE); first=True
for im in frames():
    if first: first=False
    pr.stdin.write(np.asarray(im).tobytes())
pr.stdin.close(); pr.wait()
# Cover = erste Textszene bei voller Deckkraft
sc0=spec['scenes'][0]; p=PAL[sc0.get('pal','BL')]; cv=bgs[sc0.get('pal','BL')].copy()
draw_text(cv,sc0['text'],sc0.get('accent'),sc0.get('fs',96),W//2,H//2-40,p['fg'],1.0,p['ac']); cv.save(OUT/'cover.png')
print('ok',OUT)
