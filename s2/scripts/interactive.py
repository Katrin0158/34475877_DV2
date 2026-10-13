# Adds Week 10 style interactions to the generated specs (run after specs2.py)
import json
def load(n):return json.load(open(f's2/js/{n}.json'))
def save(n,d):json.dump(d,open(f's2/js/{n}.json','w'),indent=2,ensure_ascii=False)
# 1) Map 2: year slider (bound range parameter, like the house-price map)
m=load('map2_symbols')
m['title']="Total box office of films made in each country, up to the chosen year"
m['params']=[{"name":"Year_selection","value":2016,"bind":{"input":"range","min":1950,"max":2016,"step":1,"name":"Films released up to: "}}]
c=m['layer'][3]
c['data']={"url":"data/film_country.csv"}
c['transform']=[{"filter":"datum.year<=Year_selection"},
 {"aggregate":[{"op":"sum","field":"revenue","as":"Box office"},{"op":"count","as":"Films"}],"groupby":["Country","longitude","latitude"]},
 {"filter":"datum['Box office']>0"}]
c['mark']={"type":"circle","opacity":0.75,"color":"#e8a838","stroke":"#fff3c4","strokeWidth":0.6}
c['encoding']={"longitude":{"field":"longitude","type":"quantitative"},"latitude":{"field":"latitude","type":"quantitative"},
 "size":{"field":"Box office","type":"quantitative","title":"Box office (US$)","scale":{"type":"sqrt","domain":[0,400000000000],"range":[0,3500]},"legend":{"format":"~s"}},
 "tooltip":[{"field":"Country"},{"field":"Box office","type":"quantitative","format":",.0f"},{"field":"Films","type":"quantitative"}]}
save('map2_symbols',m)
# 2) Streamgraph: click a genre in the legend to highlight it
s=load('chart4_stream')
s['params']=[{"name":"genre_pick","select":{"type":"point","fields":["genre"]},"bind":"legend"}]
s['encoding']['opacity']={"condition":{"param":"genre_pick","value":1},"value":0.25}
save('chart4_stream',s)
# 3) Scatter: click an era in the legend to highlight it
t=load('chart8_scatter')
t['layer'][0]['params']=[{"name":"era_pick","select":{"type":"point","fields":["era"]},"bind":"legend"}]
t['layer'][0]['encoding']['opacity']={"condition":{"param":"era_pick","value":0.9},"value":0.08}
save('chart8_scatter',t)
