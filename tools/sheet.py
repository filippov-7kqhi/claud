import cairosvg, glob, os, base64, sys
d=sys.argv[1]; out=sys.argv[2]
files=sorted(glob.glob(d+'/*.svg'))
rows=[]
for i,f in enumerate(files):
    png=f'/tmp/cs_{i}.png'
    cairosvg.svg2png(url=f, write_to=png, output_width=560)
    b=base64.b64encode(open(png,'rb').read()).decode()
    x=(i%2)*570; y=(i//2)*365
    rows.append(f'<g transform="translate({x},{y})"><image href="data:image/png;base64,{b}" width="560" height="355"/></g>')
h=365*((len(files)+1)//2)
open('/tmp/_s.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1140" height="{h}"><rect width="100%" height="100%" fill="#888"/>{"".join(rows)}</svg>')
cairosvg.svg2png(url='/tmp/_s.svg', write_to=out, output_width=1140)
print('ok', len(files))
