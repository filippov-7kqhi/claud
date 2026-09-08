import sys, os, glob
from playwright.sync_api import sync_playwright
root=sys.argv[1]; outdir=sys.argv[2]; pages=sys.argv[3].split(',')
w=int(sys.argv[4]) if len(sys.argv)>4 else 1360
os.makedirs(outdir, exist_ok=True)
errs=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                         args=['--no-sandbox','--disable-dev-shm-usage'])
    for p in pages:
        pg=b.new_page(viewport={'width':w,'height':1000})
        pg.on('console', lambda m: errs.append(f'{p}: console {m.type}: {m.text}') if m.type=='error' else None)
        pg.on('pageerror', lambda ex: errs.append(f'{p}: pageerror {ex}'))
        pg.goto('file://'+os.path.join(root,p), wait_until='load')
        pg.wait_for_timeout(900)
        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(700)
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(outdir,p.replace('.html','')+f'-{w}.png'), full_page=True)
        # broken images
        bad=pg.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'))")
        if bad: errs.append(f'{p}: broken images {bad}')
        ow=pg.evaluate("document.documentElement.scrollWidth")
        if ow > w+2: errs.append(f'{p}: horizontal overflow scrollWidth={ow} viewport={w}')
        pg.close()
    b.close()
print('\n'.join(errs) if errs else 'NO ERRORS')
