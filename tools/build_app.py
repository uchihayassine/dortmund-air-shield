"""Build the Air Shield Planner: app/planner.template.html + data -> app/air-shield-planner-en.html."""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = (ROOT / "data" / "airshield_data.json").read_text(encoding="utf-8")
bm = json.loads((ROOT / "data" / "basemap" / "basemap.json").read_text(encoding="utf-8"))
for k in ("dark", "light"):
    bm[k] = "data:image/jpeg;base64," + base64.b64encode((ROOT / "data" / "basemap" / f"basemap_{k}.jpg").read_bytes()).decode()

html = (ROOT / "app" / "planner.template.html").read_text(encoding="utf-8")
html = html.replace("/*__DATA__*/", data).replace("/*__BASEMAP__*/", json.dumps(bm))
out = ROOT / "app" / "air-shield-planner-en.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
