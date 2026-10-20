# A Century of Cinema (FIT3179 Data Visualisation 2)

Layout follows the Week 8–10 example repositories:
- `index.html` – page and story text, one `<div>` per chart; `js/vega_lite_vis.js` holds the `vegaEmbed(...)` calls
- `css/layout.css` – short stylesheet (colours and text); the grid comes from Pure.css
- `js/` – one human-readable Vega-Lite JSON file per chart
- `data/` – CSV and TopoJSON data
- `scripts/` – Python used to prepare the CSV files and generate the JSON specs

| File in `js/` | Idea from the lecture notes |
|---|---|
| map1_choropleth.json | Week 8 choropleth: TopoJSON + `lookup` on `properties.NAME` from a CSV, `calculate` to normalise per million people, `threshold` colour scale, ocean and graticule layers |
| map2_symbols.json | Week 8 proportional symbol map: `circle` marks placed with longitude/latitude, size = box office, colour = rating |
| map3_flow.json | Layered `geoshape` lines (GeoJSON) for co-production links |
| chart4–chart14 | Streamgraph, heatmap, radar (5 genres, 5 measures), density (row facet), scatter, studio lollipop, annotated line chart, highlighted bar chart, genre-pair matrix, boxplot by rating band, profit bars |

Data: TMDB 5000 Movie Dataset (Kaggle); World Bank SP.POP.TOTL (2016); Natural Earth 1:110m countries, oceans and graticules (FIT3179 example repository).
Preview locally with `python3 -m http.server` inside this folder.
