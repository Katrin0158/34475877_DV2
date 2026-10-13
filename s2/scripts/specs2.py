import json,re
S='https://vega.github.io/schema/vega-lite/v5.json'
CFG=json.load(open('site/specs/config.json'))
def w(n,d):
    d={"$schema":S,**{k:v for k,v in d.items() if k!="$schema"},"config":CFG}
    json.dump(d,open(f's2/js/{n}.json','w'),indent=2,ensure_ascii=False)
CT='data/ne_110m_admin_0_countries.topojson'
countries={"data":{"url":CT,"format":{"type":"topojson","feature":"ne_110m_admin_0_countries"}}}
base={**countries,"mark":{"type":"geoshape","fill":"#3a342d","stroke":"#14110f","strokeWidth":0.4}}
ocean={"data":{"url":"data/oceans.topojson","format":{"type":"topojson","feature":"oceans"}},"mark":{"type":"geoshape","fill":"#17222b"}}
grat={"data":{"url":"data/WorldMapWithGraticules.topojson","format":{"type":"topojson","feature":"ne_110m_graticules_30"}},"mark":{"type":"geoshape","fill":None,"stroke":"#2f3a44","strokeWidth":0.5}}
proj={"type":"equalEarth"}
lookup=lambda fields:{"lookup":"properties.NAME","from":{"data":{"url":"data/countries.csv"},"key":"Country","fields":fields}}
# --- Week 8 style maps -------------------------------------------------
w('map1_choropleth',{"title":"Films per million people, by production country","width":"container","height":400,"projection":proj,
 "layer":[ocean,grat,base,{**countries,"transform":[lookup(["Films","Population"]),{"filter":"datum.Films>0 && datum.Population>0"},
  {"calculate":"datum.Films/datum.Population*1000000","as":"Films per million people"}],
  "mark":{"type":"geoshape","stroke":"#14110f","strokeWidth":0.4},
  "encoding":{"color":{"field":"Films per million people","type":"quantitative","scale":{"type":"threshold","domain":[0.05,0.25,1,3,8],"range":["#4a3a2a","#7a5a2a","#b07a26","#e8a838","#f6d27a","#fff3c4"]},"legend":{"format":".2f"}},
   "tooltip":[{"field":"properties.NAME","type":"nominal","title":"Country"},{"field":"Films","type":"quantitative"},{"field":"Films per million people","type":"quantitative","format":".2f"}]}}]})
w('map2_symbols',{"title":"Total box office of films made in each country","width":"container","height":400,"projection":proj,
 "layer":[ocean,grat,base,{"data":{"url":"data/countries.csv"},"transform":[{"filter":"datum.Revenue>0"}],
  "mark":{"type":"circle","opacity":0.75,"stroke":"#fff3c4","strokeWidth":0.6},
  "encoding":{"longitude":{"field":"longitude","type":"quantitative"},"latitude":{"field":"latitude","type":"quantitative"},
   "size":{"field":"Revenue","type":"quantitative","title":"Box office (US$)","scale":{"type":"sqrt","range":[10,3500]},"legend":{"format":"~s"}},
   "color":{"field":"Rating","type":"quantitative","title":"Average rating","scale":{"scheme":"goldorange","domain":[5.5,7]}},
   "tooltip":[{"field":"Country"},{"field":"Revenue","type":"quantitative","format":",.0f"},{"field":"Films"},{"field":"Rating","format":".2f"}]}}]})
w('map3_flow',{"title":"Countries that make films together","width":"container","height":400,"projection":proj,
 "layer":[ocean,grat,base,{"data":{"url":"data/links.geojson","format":{"type":"json","property":"features"}},
  "mark":{"type":"geoshape","filled":False,"strokeCap":"round"},
  "encoding":{"stroke":{"value":"#e8a838"},"opacity":{"value":0.6},"strokeWidth":{"field":"properties.count","type":"quantitative","title":"Joint films","scale":{"type":"sqrt","range":[0.6,9]}},
   "tooltip":[{"field":"properties.pair","title":"Countries"},{"field":"properties.count","title":"Joint films"}]}}]})
# --- Week 10 style coordinated views (brush on the line chart) ----------
top8=["Drama","Comedy","Thriller","Action","Romance","Adventure","Crime","Horror"]
w('multiview',{"vconcat":[
 {"width":"container","height":330,"title":"Where were the films made? (drag on the line chart below)","projection":proj,
  "layer":[ocean,grat,base,{"data":{"url":"data/film_country.csv"},
   "transform":[{"filter":{"param":"time_brush"}},{"aggregate":[{"op":"count","as":"Films"}],"groupby":["Country","longitude","latitude"]}],
   "mark":{"type":"circle","opacity":0.7,"color":"#e8a838","stroke":"#fff3c4","strokeWidth":0.5},
   "encoding":{"longitude":{"field":"longitude","type":"quantitative"},"latitude":{"field":"latitude","type":"quantitative"},
    "size":{"field":"Films","type":"quantitative","scale":{"type":"sqrt","range":[10,2500]},"legend":{"title":"Films in period"}},
    "tooltip":[{"field":"Country"},{"field":"Films","type":"quantitative"}]}}]},
 {"width":"container","height":60,"title":"Drag across the years to filter the map and the genre chart","data":{"url":"data/movies.csv"},
  "params":[{"name":"time_brush","value":{"x":[1990,2016]},"select":{"type":"interval","encodings":["x"]}}],"mark":{"type":"line","color":"#e8a838"},
  "encoding":{"x":{"field":"year","type":"quantitative","axis":{"title":"","format":"d"},"scale":{"domain":[1950,2017]}},"y":{"aggregate":"count","title":"Films","axis":{"tickCount":3,"grid":False}}}},
 {"width":"container","height":200,"data":{"url":"data/genre_long.csv"},"transform":[{"filter":{"field":"genre","oneOf":top8}}],"mark":"area",
  "encoding":{"x":{"field":"year","type":"quantitative","scale":{"domain":{"param":"time_brush"}},"axis":{"title":"","format":"d","tickCount":6,"grid":False}},
   "y":{"aggregate":"count","title":"Films per genre"},"color":{"field":"genre","type":"nominal","scale":{"domain":top8,"scheme":"tableau10"},"legend":{"title":"Genre"}}}}]})
# --- remaining charts: reuse earlier specs, now reading CSV ------------
for n in ['chart4_stream','chart5_heatmap','chart6_boxplot','chart7_density','chart8_scatter','chart9_studios','chart10_runtime','chart11_months']:
    s=open(f'site/specs/{n}.json').read()
    s=s.replace('data/genre_long.json','data/genre_long.csv').replace('data/movies.json','data/movies.csv').replace('data/studios.json','data/studios.csv')
    w(n,json.loads(s))
