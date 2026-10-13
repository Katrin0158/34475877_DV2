import pandas as pd, json, ast, pycountry
D='s2/data/'
# ---------- data prep (lecturer style: CSV files) ----------
m=pd.read_csv('data/tmdb_5000_movies.csv');m=m[m.status=='Released'].copy()
d=pd.to_datetime(m.release_date,errors='coerce');m['year']=d.dt.year;m['month']=d.dt.month;m=m.dropna(subset=['year']);m['year']=m.year.astype(int);m['decade']=m.year//10*10
P=lambda s:ast.literal_eval(s) if isinstance(s,str) else []
m['g']=m.genres.map(lambda s:[x['name'] for x in P(s)]);m['c']=m.production_countries.map(lambda s:[x['iso_3166_1'] for x in P(s)])
m['rev']=m.revenue.where(m.revenue>1e4);m['bud']=m.budget.where(m.budget>1e4);m['roi']=(m.rev/m.bud).round(2)
m['runtime']=m.runtime.where(m.runtime>0)
mv=m[m.vote_count>=10]
mv[['title','year','decade','month','vote_average','runtime','bud','rev','roi']].rename(columns={'vote_average':'rating','bud':'budget','rev':'revenue'}).to_csv(D+'movies.csv',index=False)
gl=mv.explode('g').dropna(subset=['g'])[['title','g','year','decade','vote_average','roi']].rename(columns={'g':'genre','vote_average':'rating'});gl.to_csv(D+'genre_long.csv',index=False)
# country names must match Natural Earth properties.NAME (for lookup)
t=json.load(open(D+'ne_110m_admin_0_countries.topojson'))['objects']['ne_110m_admin_0_countries']['geometries']
ne={g['properties']['ISO_A3_EH']:g['properties']['NAME'] for g in t};ne.update({g['properties']['ADM0_A3']:g['properties']['NAME'] for g in t})
old=pd.DataFrame(json.load(open('site/data/countries.json')))  # lon/lat centroids + stats computed earlier
pop=pd.read_csv('/mnt/user-data/uploads/API_SP_POP_TOTL_DS2_en_csv_v2_5254.csv',skiprows=4).set_index('Country Code')['2016']
rows=[];miss=[]
for r in old.itertuples():
    a3=pycountry.countries.get(alpha_2=r.iso2).alpha_3;n=ne.get(a3)
    if not n:
        if r.films>=5:miss.append((r.name,r.films))
        continue
    rows.append(dict(Country=n,iso2=r.iso2,Films=r.films,Revenue=r.revenue,Rating=r.rating,Population=pop.get(a3),FilmsPerMillion=r.per_million,longitude=r.lon,latitude=r.lat))
pd.DataFrame(rows).to_csv(D+'countries.csv',index=False);print('unmatched >=5 films:',miss)
iso2n={x['iso2']:x['Country'] for x in rows};cen={x['iso2']:(x['longitude'],x['latitude']) for x in rows}
fc=[dict(title=r.title,year=r.year,Country=iso2n[c],longitude=cen[c][0],latitude=cen[c][1],revenue=r.rev) for r in m.itertuples() for c in set(r.c) if c in iso2n and cen[c][0]==cen[c][0]]
pd.DataFrame(fc).to_csv(D+'film_country.csv',index=False)
import shutil
for f in ['studios.json','links.geojson']:shutil.copy('site/data/'+f,D+f)
pd.DataFrame(json.load(open('site/data/studios.json'))).to_csv(D+'studios.csv',index=False)
