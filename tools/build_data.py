"""Build the Air Shield planning dataset from Dortmund open data.

Inputs (data/raw, downloaded from open-data.dortmund.de):
  fb62-statistischebezirke.geojson   62 statistical districts (polygons)
  pop2023.json                       population per statistical district, 2023
  feuerwehr.geojson / polizei.geojson / krankenhaus.geojson   point layers

Output: data/airshield_data.json  (demand grid, candidate sites, context layers)

Assumption: population is spread evenly inside each statistical district.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CELL_KM = 0.6                      # demand grid resolution
LAT0, LON0 = 51.51, 7.46           # local projection origin
KX, KY = 111.32 * math.cos(math.radians(LAT0)), 110.57


def load(name):
    return json.loads((RAW / name).read_text(encoding="utf-8"))


def to_xy(lon, lat):
    return (lon - LON0) * KX, (lat - LAT0) * KY


def to_ll(x, y):
    return LON0 + x / KX, LAT0 + y / KY


def rings(geom):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return [p for p in polys]          # list of polygons, each = [outer, holes...]


def inside(pt, poly):
    """Even-odd rule over all rings of one polygon (holes handled naturally)."""
    x, y = pt
    hit = False
    for ring in poly:
        for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                hit = not hit
    return hit


# --- districts + population -------------------------------------------------
pop = {r["unterbezirk_nr"]: r["insgesamt_zusammen"] for r in load("pop2023.json") if r["unterbezirk_nr"]}
districts = []
for f in load("fb62-statistischebezirke.geojson")["features"]:
    p = f["properties"]
    nr = p["statistischer_bezirk_nr"]
    polys_xy = [[[to_xy(*c) for c in ring] for ring in poly] for poly in rings(f["geometry"])]
    districts.append({
        "nr": nr, "name": p["statistischer_bezirk"], "sb": p["stadtbezirk_bezeichnung"] if "stadtbezirk_bezeichnung" in p else p["stadtbezbezirk_bezeichnung"],
        "pop": pop.get(nr, 0),
        "geom": [[[[round(c[0], 5), round(c[1], 5)] for c in ring] for ring in poly] for poly in rings(f["geometry"])],
        "_xy": polys_xy,
    })

# --- demand grid ------------------------------------------------------------
allx = [c[0] for d in districts for poly in d["_xy"] for c in poly[0]]
ally = [c[1] for d in districts for poly in d["_xy"] for c in poly[0]]
# Honeycomb: pointy-top hexagons with the same area as a CELL_KM square.
HEX_R = math.sqrt(CELL_KM ** 2 / (1.5 * math.sqrt(3)))   # circumradius, km
HEX_W, HEX_H = math.sqrt(3) * HEX_R, 1.5 * HEX_R          # column / row spacing
cells = []
row, y = 0, min(ally) + HEX_R
while y < max(ally):
    x = min(allx) + HEX_W / 2 + (HEX_W / 2 if row % 2 else 0)
    while x < max(allx):
        for di, d in enumerate(districts):
            if any(inside((x, y), poly) for poly in d["_xy"]):
                cells.append({"x": x, "y": y, "d": di})
                break
        x += HEX_W
    y += HEX_H
    row += 1

per_district = {}
for c in cells:
    per_district[c["d"]] = per_district.get(c["d"], 0) + 1
for c in cells:
    d = districts[c["d"]]
    c["pop"] = round(d["pop"] / per_district[c["d"]])

# Event / traffic hotspots get extra mission weight (coordinates approximate).
HOTSPOTS = [
    ("Signal Iduna Park", 51.4926, 7.4518, 20000),
    ("Westfalenhallen", 51.4957, 7.4573, 8000),
    ("Hauptbahnhof", 51.5178, 7.4593, 12000),
    ("Phoenix-See", 51.4878, 7.5110, 5000),
    ("Hafen Dortmund", 51.5320, 7.4380, 6000),
    ("Flughafen Dortmund", 51.5183, 7.6122, 6000),
    ("TU Dortmund", 51.4925, 7.4141, 5000),
    ("Westfalenpark", 51.4990, 7.4730, 4000),
]

# --- candidate sites (BOS properties: power, access control, staffed) -------
cands, seen = [], set()
for layer, kind in (("feuerwehr.geojson", "fire"), ("polizei.geojson", "police")):
    for f in load(layer)["features"]:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"][:2]
        key = (round(lat, 4), round(lon, 4))
        name = p["objektname"]
        if key in seen or "Lünen" in name or "Wasserschutz" in name:
            continue
        if name == "Freiwillige Feuerwehr":
            name = f"Freiwillige Feuerwehr {p.get('statbezibe') or ''}".strip()
        seen.add(key)
        prof = "volunteer" if name.startswith("Freiwillige") else kind
        cands.append({"name": name, "kind": prof, "lat": round(lat, 5), "lon": round(lon, 5),
                      "ward": p.get("statbezibe")})

hospitals = [
    {"name": f["properties"]["objektname"], "lat": round(f["geometry"]["coordinates"][1], 5),
     "lon": round(f["geometry"]["coordinates"][0], 5)}
    for f in load("krankenhaus.geojson")["features"]
    if f["properties"]["objektart"] == "KrankenhausKlinik"
]

out = {
    "meta": {
        "source": "open-data.dortmund.de (statistische Bezirke, Bevölkerung 2023, Feuerwehr, Polizei, Krankenhäuser)",
        "cell_km": CELL_KM, "hex_r_km": round(HEX_R, 4), "population": sum(d["pop"] for d in districts),
        "origin": [LAT0, LON0],
    },
    "districts": [{k: v for k, v in d.items() if k != "_xy"} for d in districts],
    "cells": [[round(to_ll(c["x"], c["y"])[1], 5), round(to_ll(c["x"], c["y"])[0], 5), c["pop"], c["d"]] for c in cells],
    "hotspots": [{"name": n, "lat": la, "lon": lo, "w": w} for n, la, lo, w in HOTSPOTS],
    "candidates": cands,
    "hospitals": hospitals,
    "airport": {"name": "Flughafen Dortmund (DTM)", "lat": 51.5183, "lon": 7.6122},
}
(ROOT / "data" / "airshield_data.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"districts={len(districts)} cells={len(cells)} pop={out['meta']['population']} "
      f"candidates={len(cands)} hospitals={len(hospitals)}")
