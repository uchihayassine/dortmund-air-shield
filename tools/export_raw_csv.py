"""Write the raw open-data inputs as CSV: population table and point layers (fire, police, hospitals).

python tools/export_raw_csv.py  ->  data/export/raw_*.csv
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "export"
OUT.mkdir(parents=True, exist_ok=True)

rows = json.loads((RAW / "pop2023.json").read_text(encoding="utf-8"))
keys = list(rows[0].keys())
with open(OUT / "raw_population_2023.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
print("raw_population_2023.csv:", len(rows), "rows")

for name in ("feuerwehr", "polizei", "krankenhaus"):
    feats = json.loads((RAW / f"{name}.geojson").read_text(encoding="utf-8"))["features"]
    props = sorted({k for ft in feats for k in ft["properties"]})
    with open(OUT / f"raw_{name}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["lon", "lat"] + props)
        for ft in feats:
            lon, lat = ft["geometry"]["coordinates"][:2]
            w.writerow([lon, lat] + [ft["properties"].get(k, "") for k in props])
    print(f"raw_{name}.csv:", len(feats), "rows")
