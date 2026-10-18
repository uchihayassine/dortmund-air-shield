"""Download OpenStreetMap tiles (© OpenStreetMap contributors) for Dortmund once and stitch them.

The dark variant is derived from the same tiles (inverted, desaturated, tinted to the planner palette).

Outputs data/basemap/basemap_{dark,light}.jpg plus basemap.json with the image's lon/lat bounds
(Web Mercator, so a d3.geoMercator projection can place it with two corner points).
"""
import io
import json
import math
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "basemap"
OUT.mkdir(parents=True, exist_ok=True)
Z = 13
LON0, LON1, LAT0, LAT1 = 7.29, 7.65, 51.40, 51.61       # Dortmund plus margin



def tile_xy(lon, lat, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def tile_lonlat(x, y, z):
    n = 2 ** z
    lon = x / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lon, lat


fx0, fy0 = tile_xy(LON0, LAT1, Z)
fx1, fy1 = tile_xy(LON1, LAT0, Z)
tx0, ty0, tx1, ty1 = int(fx0), int(fy0), int(fx1), int(fy1)
canvas = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
for tx in range(tx0, tx1 + 1):
    for ty in range(ty0, ty1 + 1):
        url = f"https://tile.openstreetmap.org/{Z}/{tx}/{ty}.png"
        req = urllib.request.Request(url, headers={"User-Agent": "AirShieldHackathon/1.0 (DO-Data-Hackathon prototype, one-off download)"})
        canvas.paste(Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert("RGB"), ((tx - tx0) * 256, (ty - ty0) * 256))
        time.sleep(0.2)
box = (round((fx0 - tx0) * 256), round((fy0 - ty0) * 256), round((fx1 - tx0) * 256), round((fy1 - ty0) * 256))
light = ImageEnhance.Color(canvas.crop(box)).enhance(0.55)
dark = ImageOps.invert(ImageEnhance.Color(canvas.crop(box)).enhance(0.15))
dark = Image.blend(dark, Image.new("RGB", dark.size, (14, 22, 32)), 0.35)     # tint toward the planner navy
dark = ImageEnhance.Contrast(ImageEnhance.Brightness(dark).enhance(1.23)).enhance(1.15)
for name, img in (("light", light), ("dark", dark)):
    img.save(OUT / f"basemap_{name}.jpg", quality=80, optimize=True)
    print(name, img.size, (OUT / f"basemap_{name}.jpg").stat().st_size // 1024, "KB")

west, north = tile_lonlat(tx0 + box[0] / 256, ty0 + box[1] / 256, Z)
east, south = tile_lonlat(tx0 + box[2] / 256, ty0 + box[3] / 256, Z)
(OUT / "basemap.json").write_text(json.dumps({"west": west, "north": north, "east": east, "south": south,
                                              "attribution": "© OpenStreetMap contributors"}), encoding="utf-8")
print("bounds", west, north, east, south)
