"""Beispiel-Layouts (Mythos/Fakt, Serif-Zitat, Atem-Infografik, Foto-Cover-Platzhalter, Koerpercheck). python3 tools/render_examples.py"""
import sys, pathlib, math
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from topo import slide_paths
from playwright.sync_api import sync_playwright
OUT=ROOT/'examples'; OUT.mkdir(exist_ok=True)
SANS="font-family:'Nunito Sans','Inter',sans-serif"
SERIF="font-family:'Libre Baskerville',Georgia,serif;font-style:italic"
def topo(i,c1,c2,zoom=1.0):
    s,f=slide_paths(i)
    return f'<svg viewBox="0 0 1080 1350" width="1080" height="1350" style="position:absolute;left:0;top:0;transform:scale({zoom});transform-origin:50% 50%" fill="none" stroke-width="{3/zoom:.2f}" stroke-linecap="round"><path stroke="{c1}" d="{s}"/><path stroke="{c2}" d="{f}"/></svg>'
def frame(bg,inner,fg):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}</style></head><body><div style="position:relative;overflow:hidden;width:1080px;height:1350px;background:{bg};color:{fg};{SANS}">{inner}</div></body></html>'
W="rgba(255,255,255,0.28)";W2="rgba(255,255,255,0.14)"
def header(n,t,col): return f'<div style="position:absolute;left:96px;right:96px;top:96px;display:flex;justify-content:space-between;font-size:28px;letter-spacing:1px;color:{col}"><span>@jens.lovelifenow</span><span>{n} / {t}</span></div>'

# 1 Mythos/Fakt: geteilt
mf=f'''<div style="position:absolute;inset:0 0 50% 0;background:#DCE6F5;overflow:hidden">{topo(1,"#FFFFFF","rgba(255,255,255,0.6)",1.6)}</div>
<div style="position:absolute;inset:50% 0 0 0;background:#2D5AAA;overflow:hidden">{topo(2,W,W2)}</div>
{header(2,6,"#1B3470")}
<div style="position:absolute;left:96px;right:96px;top:250px;color:#1B3470"><div style="font-size:34px;font-weight:700;letter-spacing:3px;opacity:.7">MYTHOS</div>
<div style="font-size:78px;font-weight:700;line-height:1.1;margin-top:28px;text-decoration:line-through;text-decoration-thickness:8px;text-decoration-color:#2D5AAA;opacity:.55">„Ich verliere die Kontrolle.“</div></div>
<div style="position:absolute;left:96px;right:96px;top:760px;color:#fff"><div style="font-size:34px;font-weight:700;letter-spacing:3px;opacity:.8">FAKT</div>
<div style="font-size:92px;font-weight:700;line-height:1.1;margin-top:28px">Du bleibst bei dir.</div>
<div style="font-size:38px;font-weight:300;line-height:1.4;margin-top:32px;max-width:800px">Wird dein Bewusstsein gebraucht, ist es sofort da.</div></div>
<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:120px;height:120px;border-radius:60px;background:#F8EEE8;color:#2D5AAA;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:700">↓</div>'''

# 2 Serif-Zitat
zi=f'''{topo(5,W,W2,1.35)}{header(3,6,"#DCE6F5")}
<div style="position:absolute;left:96px;top:300px;font-size:300px;{SERIF};color:#DCE6F5;opacity:.35;line-height:1">“</div>
<div style="position:absolute;left:96px;right:96px;top:470px;{SERIF};font-size:76px;line-height:1.3;color:#fff">Das andere Boot ist leer.</div>
<div style="position:absolute;left:96px;right:96px;top:760px;font-size:38px;font-weight:300;line-height:1.5;color:#DCE6F5;max-width:760px">Oft suchen wir einen Schuldigen. Spannender ist die Frage: Wie gehe ich mit mir um, wenn es kracht?</div>
<div style="position:absolute;left:96px;bottom:96px;font-size:32px;color:#DCE6F5">Eine alte buddhistische Geschichte</div>'''

# 3 Atem-Infografik: Welle 4 ein / 6 aus
def wave():
    x0,x1,y0,amp=96,984,0,150
    pts=[];n=200
    for k in range(n+1):
        t=k/n; x=x0+(x1-x0)*t
        # 4/10 ein, 6/10 aus
        if t<0.4: ph=t/0.4*math.pi; y=-math.sin(ph/2)**2*2  # 0->1? 
        u=t/0.4 if t<0.4 else (t-0.4)/0.6
        v=(1-math.cos(math.pi*u))/2
        yv=v if t<0.4 else 1-v
        pts.append((x,900-amp*2*yv))
    d="M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    return d
xi=96+888*0.4
ig=f'''{topo(9,"rgba(255,255,255,0.7)","rgba(255,255,255,0.35)")}{header(3,6,"#2D5AAA")}
<div style="position:absolute;left:96px;right:96px;top:240px;color:#2D5AAA"><div style="font-size:36px;font-weight:700">Mini-Ritual</div><div style="font-size:84px;font-weight:700;line-height:1.1;margin-top:24px">Länger aus&shy;atmen als ein&shy;atmen.</div></div>
<svg viewBox="0 0 1080 1350" width="1080" height="1350" style="position:absolute;left:0;top:0" fill="none">
<path d="{wave()}" stroke="#2D5AAA" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="{xi}" y1="600" x2="{xi}" y2="920" stroke="#2D5AAA" stroke-width="3" stroke-dasharray="10 12" opacity=".5"/></svg>
<div style="position:absolute;left:96px;top:950px;color:#2D5AAA"><div style="font-size:120px;font-weight:700;line-height:1">4</div><div style="font-size:34px;font-weight:700;margin-top:4px">Sekunden ein</div></div>
<div style="position:absolute;left:{xi+40}px;top:950px;color:#2D5AAA"><div style="font-size:120px;font-weight:700;line-height:1">6</div><div style="font-size:34px;font-weight:700;margin-top:4px">Sekunden aus</div></div>
<div style="position:absolute;left:96px;right:96px;bottom:70px;font-size:34px;font-weight:300;color:#1B3470;line-height:1.4">Fünf Minuten lang. Ein langes Ausatmen kann helfen, runterzufahren.</div>'''

# 4 Foto-Cover-Platzhalter
fo=f'''<div style="position:absolute;inset:0;background:linear-gradient(160deg,#9fb6dd 0%,#6f8fc6 100%)"></div>
<div style="position:absolute;left:0;right:0;top:0;height:880px;display:flex;align-items:center;justify-content:center;font-size:36px;color:rgba(255,255,255,.75);border-bottom:2px dashed rgba(255,255,255,.5)">[ Foto von Jens ]</div>
<div style="position:absolute;inset:auto 0 0 0;height:560px;background:#1B3470;overflow:hidden">{topo(3,"rgba(220,230,245,0.30)","rgba(220,230,245,0.14)",1.2)}</div>
<div style="position:absolute;left:96px;right:96px;top:800px;color:#fff"><div style="font-size:34px;font-weight:700;color:#DCE6F5">Hypnose</div>
<div style="font-size:78px;font-weight:700;line-height:1.1;margin-top:20px">3 Dinge, die viele falsch denken.</div></div>
<div style="position:absolute;left:96px;top:96px;font-size:28px;color:#fff;letter-spacing:1px">@jens.lovelifenow</div>'''

# 5 Koerpercheck: Silhouette
si=f'''{topo(7,"#FFFFFF","rgba(255,255,255,0.6)",1.5)}{header(2,6,"#2D5AAA")}
<div style="position:absolute;left:96px;top:240px;color:#1B3470"><div style="font-size:34px;font-weight:700;color:#2D5AAA">Körpercheck</div><div style="font-size:72px;font-weight:700;line-height:1.1;margin-top:18px;max-width:520px">Drei Stress-Signale</div></div>
<svg viewBox="0 0 1080 1350" width="1080" height="1350" style="position:absolute;left:0;top:0" fill="none">
<circle cx="760" cy="420" r="95" fill="#2D5AAA"/>
<path d="M 600 640 Q 600 540 760 540 Q 920 540 920 640 L 940 1000 L 580 1000 Z" fill="#2D5AAA"/>
<circle cx="640" cy="590" r="30" fill="#F8EEE8" stroke="#1B3470" stroke-width="5"/><circle cx="880" cy="590" r="30" fill="#F8EEE8" stroke="#1B3470" stroke-width="5"/>
<circle cx="760" cy="700" r="30" fill="#F8EEE8" stroke="#1B3470" stroke-width="5"/><circle cx="760" cy="468" r="26" fill="#F8EEE8" stroke="#1B3470" stroke-width="5"/>
<line x1="640" y1="590" x2="400" y2="590" stroke="#1B3470" stroke-width="4"/><line x1="760" y1="700" x2="400" y2="700" stroke="#1B3470" stroke-width="4"/><line x1="734" y1="468" x2="400" y2="470" stroke="#1B3470" stroke-width="4"/></svg>
<div style="position:absolute;left:96px;top:555px;font-size:36px;font-weight:700;color:#1B3470;width:300px">01 Schultern<br><span style="font-weight:300;font-size:30px">wandern hoch</span></div>
<div style="position:absolute;left:96px;top:665px;font-size:36px;font-weight:700;color:#1B3470;width:300px">02 Atem<br><span style="font-weight:300;font-size:30px">sitzt in der Brust</span></div>
<div style="position:absolute;left:96px;top:435px;font-size:36px;font-weight:700;color:#1B3470;width:300px;display:none">03 Kiefer</div>
<div style="position:absolute;left:96px;bottom:96px;font-size:38px;font-weight:300;color:#1B3470">03 Kiefer: fest, Zähne aufeinander.</div>'''

jobs=[("beispiel_1_mythos_fakt","#2D5AAA",mf,"#fff"),("beispiel_2_zitat","#1B3470",zi,"#fff"),("beispiel_3_atem_infografik","#F8EEE8",ig,"#2D5AAA"),("beispiel_4_foto_cover","#1B3470",fo,"#fff"),("beispiel_5_koerpercheck","#DCE6F5",si,"#1B3470")]
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=br.new_page(viewport={'width':1080,'height':1350})
    for n,bg,inner,fg in jobs:
        pg.set_content(frame(bg,inner,fg)); pg.wait_for_timeout(200)
        pg.screenshot(path=str(OUT/f'{n}.png'))
    br.close()
print('ok')
