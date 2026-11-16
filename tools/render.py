"""Rendert Karussell-Slides (1080x1350) aus einer JSON-Spec.
Nutzung: python3 tools/render.py specs/<name>.json
Spec: {"name","start","pal":["BL","BS"],"serif":false,"zoom":1.0,"slides":[[label,headline,body,fontsize],...]}
Paletten: BL blau, BS blush, NV navy, LB hellblau. 'start' = Muster-Offset (pro Post um 6 erhoehen, damit das Muster weiterlaeuft).
Chrome: /usr/bin/google-chrome (Playwright, kein Netz -> Fallback-Schrift)."""
import sys, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from topo import slide_paths
from playwright.sync_api import sync_playwright
BL=dict(bg="#2D5AAA",fg="#FFFFFF",ac="#F8EEE8",c1="rgba(255,255,255,0.28)",c2="rgba(255,255,255,0.14)")
BS=dict(bg="#F8EEE8",fg="#2D5AAA",ac="#2D5AAA",c1="#FFFFFF",c2="rgba(255,255,255,0.6)")
NV=dict(bg="#1B3470",fg="#FFFFFF",ac="#DCE6F5",c1="rgba(220,230,245,0.30)",c2="rgba(220,230,245,0.14)")
LB=dict(bg="#DCE6F5",fg="#1B3470",ac="#2D5AAA",c1="#FFFFFF",c2="rgba(255,255,255,0.6)")
PAL=dict(BL=BL,BS=BS,NV=NV,LB=LB)
def html(i,n,lab,h,b,fs,P,serif,zoom,start):
    pal=P[(i-1)%2]; bg,fg,ac,c1,c2=pal['bg'],pal['fg'],pal['ac'],pal['c1'],pal['c2']
    s,f=slide_paths(start+i-1)
    svg=f'<svg viewBox="0 0 1080 1350" width="1080" height="1350" style="position:absolute;left:0;top:0;transform:scale({zoom});transform-origin:{(i*37)%100}% {(i*53)%100}%" fill="none" stroke-width="{3/zoom:.2f}" stroke-linecap="round"><path stroke="{c1}" d="{s}"/><path stroke="{c2}" d="{f}"/></svg>'
    foot=(f'<div style="position:relative;font-size:32px;color:{ac}">Weiter wischen →</div>' if i<n else
          f'<div style="position:relative;align-self:flex-start;border:2px solid {fg};padding:24px 40px;background:#FFFFFF;color:#2D5AAA;font-family:\'Libre Baskerville\',serif;font-style:italic;font-size:32px">@jens.lovelifenow</div>')
    p=f'<p style="margin:0;font-size:40px;font-weight:300;line-height:1.45;max-width:840px">{b}</p>' if b else ''
    hf="font-family:'Libre Baskerville',Georgia,serif;font-style:italic;font-weight:400;" if serif else "font-weight:700;"
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><style>body{{margin:0}}</style></head><body><div style="position:relative;overflow:hidden;width:1080px;height:1350px;box-sizing:border-box;padding:96px;display:flex;flex-direction:column;justify-content:space-between;background:{bg};color:{fg};font-family:'Nunito Sans','Inter',sans-serif"><div style="position:absolute;inset:0;overflow:hidden">{svg}</div><div style="position:relative;display:flex;justify-content:space-between;font-size:28px;letter-spacing:1px;color:{ac}"><span>@jens.lovelifenow</span><span>{i} / {n}</span></div><div style="position:relative;display:flex;flex-direction:column;gap:48px"><div style="font-size:36px;font-weight:700;color:{ac}">{lab}</div><h1 style="margin:0;{hf}font-size:{fs}px;line-height:1.15">{h}</h1>{p}</div>{foot}</div></body></html>'''

spec=json.load(open(sys.argv[1]))
OUT=ROOT/'posts'/spec['name']; OUT.mkdir(parents=True,exist_ok=True)
sl=spec['slides']; P=[PAL[k] for k in spec['pal']]
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=br.new_page(viewport={'width':1080,'height':1350})
    for i,(lab,h,b,fs) in enumerate(sl,1):
        pg.set_content(html(i,len(sl),lab,h,b,fs,P,spec.get('serif',False),spec.get('zoom',1.0),spec['start'])); pg.wait_for_timeout(200)
        pg.screenshot(path=str(OUT/f'slide_{i}.png'),clip={'x':0,'y':0,'width':1080,'height':1350})
    br.close()
print('ok',OUT)
