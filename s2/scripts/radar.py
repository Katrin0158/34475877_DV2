# Radar chart: 5 genres x 5 measures, each measure scaled 0-100 across all genres (100 = highest genre)
import json,re,ast,math,pandas as pd
m=pd.read_csv('data/tmdb_5000_movies.csv');m=m[m.status=='Released'].copy()
m['g']=m.genres.map(lambda s:[x['name'] for x in ast.literal_eval(s)])
m=m.explode('g').dropna(subset=['g'])
fin=m[(m.budget>1e4)&(m.revenue>1e4)&(m.vote_count>=10)].assign(roi=lambda d:d.revenue/d.budget)
rated=m[m.vote_count>=10]
T=pd.DataFrame({'Typical budget':fin.groupby('g').budget.median(),'Typical box office':fin.groupby('g').revenue.median(),
 'Return on budget':fin.groupby('g').roi.median(),'Average rating':rated.groupby('g').vote_average.mean(),'Number of films':rated.groupby('g').size()})
T=T[T.index.isin(fin.g.value_counts()[lambda s:s>=30].index)]
S=(T-T.min())/(T.max()-T.min())*100
M=list(T.columns);G=['Documentary','Horror','Animation','Drama','Action']
fmt={'Typical budget':lambda v:f'US${v/1e6:.0f}M','Typical box office':lambda v:f'US${v/1e6:.0f}M','Return on budget':lambda v:f'{v:.1f}×','Average rating':lambda v:f'{v:.2f} / 10','Number of films':lambda v:f'{int(v):,}'}
rows=[dict(genre=g,measure=k,idx=i,score=round(S.loc[g,k],1),actual=fmt[k](T.loc[g,k])) for g in G for i,k in enumerate(M)]
pd.DataFrame(rows).to_csv('s2/data/radar.csv',index=False);print(pd.DataFrame(rows).pivot(index='genre',columns='measure',values='score').round(0))
CFG=json.load(open('s2/js/chart7_density.json'))['config'];n=len(M)
xy=lambda r,i:(round(r*math.sin(2*math.pi*i/n),2),round(r*math.cos(2*math.pi*i/n),2))
SC={"type":"linear","domain":[-150,150]};AX=None
X=lambda f='x':{"field":f,"type":"quantitative","scale":SC,"axis":AX};Y=lambda f='y':{"field":f,"type":"quantitative","scale":SC,"axis":AX}
grid=[dict(ring=r,idx=i%n,x=xy(r,i)[0],y=xy(r,i)[1]) for r in (25,50,75,100) for i in range(n+1)]
spokes=[dict(x=0,y=0,x2=xy(100,i)[0],y2=xy(100,i)[1]) for i in range(n)]
labels=[dict(x=xy(122,i)[0],y=xy(122,i)[1],label=M[i]) for i in range(n)]
ticks=[dict(x=3,y=r+3,label=str(r)) for r in (25,50,75,100)]
spec={"$schema":"https://vega.github.io/schema/vega-lite/v5.json","width":460,"height":460,"title":"Five genres compared (100 = highest of all genres)",
 "layer":[
  {"data":{"values":grid},"mark":{"type":"line","color":"#4a4238","strokeWidth":1},"encoding":{"x":X(),"y":Y(),"detail":{"field":"ring","type":"nominal"},"order":{"field":"idx","type":"quantitative"}}},
  {"data":{"values":spokes},"mark":{"type":"rule","color":"#4a4238"},"encoding":{"x":X(),"y":Y(),"x2":{"field":"x2"},"y2":{"field":"y2"}}},
  {"data":{"values":ticks},"mark":{"type":"text","align":"left","color":"#8d8374","fontSize":10},"encoding":{"x":X(),"y":Y(),"text":{"field":"label"}}},
  {"data":{"values":labels},"mark":{"type":"text","color":"#f3ead9","fontSize":12,"fontWeight":"bold"},"encoding":{"x":X(),"y":Y(),"text":{"field":"label"}}},
  {"data":{"url":"data/radar.csv","format":{"type":"csv","parse":{"idx":"number","score":"number"}}},
   "transform":[{"calculate":"datum.score*sin(2*PI*datum.idx/5)","as":"x"},{"calculate":"datum.score*cos(2*PI*datum.idx/5)","as":"y"}],
   "encoding":{"x":X(),"y":Y(),"color":{"field":"genre","type":"nominal","title":"Genre","scale":{"domain":G,"range":["#e8a838","#4cc9f0","#f72585","#90be6d","#c77dff"]}}},
   "layer":[{"mark":{"type":"line","interpolate":"linear-closed","strokeWidth":2.5,"filled":True,"fillOpacity":0.12},"encoding":{"order":{"field":"idx","type":"quantitative"}}},
    {"mark":{"type":"circle","size":55,"opacity":1},"encoding":{"tooltip":[{"field":"genre","title":"Genre"},{"field":"measure","title":"Measure"},{"field":"actual","title":"Actual value"},{"field":"score","title":"Score (0-100)"}]}}]}],
 "config":CFG}
json.dump(spec,open('s2/js/chart6_radar.json','w'),indent=2,ensure_ascii=False)
p='s2/index.html';h=open(p).read()
h=h.replace('js/chart6_range.json','js/chart6_radar.json')
old=re.search(r'<p class="cap">Return on budget by genre.*?</p>',h,re.S).group(0)
h=h.replace(old,'<p class="cap">How to read it: each corner is one measure, and the further a genre\'s shape reaches towards a corner, the higher it scores. 100 means the highest of all 18 genres and 0 the lowest. Hover over a dot for the real value.</p>')
open(p,'w').write(h)
r=open('s2/README.md').read().replace('range chart (median and middle half per genre)','radar chart (5 genres, 5 measures)');open('s2/README.md','w').write(r)
