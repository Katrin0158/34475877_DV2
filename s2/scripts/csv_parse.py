# Tell Vega-Lite which CSV columns are numbers (otherwise some charts, e.g. the boxplot, receive text instead of numbers)
import json,glob
NUM={
 'movies.csv':['year','decade','month','rating','runtime','budget','revenue','roi'],
 'genre_long.csv':['year','decade','rating','roi'],
 'studios.csv':['films','revenue'],
 'countries.csv':['Films','Revenue','Rating','Population','FilmsPerMillion','longitude','latitude'],
 'film_country.csv':['year','longitude','latitude','revenue']}
def walk(o):
    if isinstance(o,dict):
        u=o.get('url')
        if isinstance(u,str) and u.endswith('.csv'):
            o['format']={"type":"csv","parse":{c:"number" for c in NUM[u.split('/')[-1]]}}
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
for f in glob.glob('s2/js/*.json'):
    d=json.load(open(f));walk(d);json.dump(d,open(f,'w'),indent=2,ensure_ascii=False)
