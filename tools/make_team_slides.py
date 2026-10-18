"""Build the two Team Pilots slides (drones scattered -> drones on their stations) in presentation/deck_EN.

After running, replace __MAPSRC__ in team-a.html and team-b.html with the uploaded map asset URL (see ARTIFACTS.md)."""
import json
import math
import random
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SCR = PROJ / "presentation"                     # deck lives in presentation/deck_EN
data = json.loads((PROJ / "data" / "airshield_data.json").read_text(encoding="utf-8"))
base = json.loads((PROJ / "data" / "base_stations.json").read_text(encoding="utf-8"))

# map box on the slide (right side), Web Mercator so it matches the OpenStreetMap image
MX, MY, MW, MH = 760, 128, 1032, 824
bm = json.loads((PROJ / "data" / "basemap" / "basemap.json").read_text(encoding="utf-8"))
def merc(lon, lat):                        # world coords in [0,1]
    return (lon + 180) / 360, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2
pts = [c for d in data["districts"] for poly in d["geom"] for c in poly[0]]
mxs, mys = zip(*(merc(*c) for c in pts))
scale = 0.94 * min(MW / (max(mxs) - min(mxs)), MH / (max(mys) - min(mys)))     # px per world unit
cx, cy = (max(mxs) + min(mxs)) / 2, (max(mys) + min(mys)) / 2
bx0, by0 = merc(bm["west"], bm["north"]); bx1, by1 = merc(bm["east"], bm["south"])
# the box may not reach past the downloaded map: shrink it, keep it right-aligned
W = int(min(MW, 2 * min(cx - bx0, bx1 - cx) * scale) - 2)
H = int(min(MH, 2 * min(cy - by0, by1 - cy) * scale) - 2)
ox, oy = MX + MW - W, MY + (MH - H) // 2
MW, MH = W, H
def local(lon, lat):                       # px inside the map box
    x, y = merc(lon, lat)
    return MW / 2 + (x - cx) * scale, MH / 2 + (y - cy) * scale
# crop the basemap to exactly this box
from PIL import Image
img = Image.open(PROJ / "data" / "basemap" / "basemap_dark.jpg")
fx = img.width / (bx1 - bx0); fy = img.height / (by1 - by0)
wx0, wy0 = cx - MW / 2 / scale, cy - MH / 2 / scale
wx1, wy1 = cx + MW / 2 / scale, cy + MH / 2 / scale
crop = img.crop((round((wx0 - bx0) * fx), round((wy0 - by0) * fy), round((wx1 - bx0) * fx), round((wy1 - by0) * fy)))
crop.resize((round(MW * 1.5), round(MH * 1.5)), Image.LANCZOS).save(SCR / "deck_EN" / "team_map_dark.jpg", quality=84, optimize=True)
km_per_px = 40075 * math.cos(math.radians(51.51)) / scale             # for coverage ring radius
scale_km = 1 / km_per_px

def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) or 1e-9
    i, dmax = 0, -1
    for k in range(1, len(pts) - 1):
        d = abs(dy * pts[k][0] - dx * pts[k][1] + bx * ay - by * ax) / n
        if d > dmax:
            i, dmax = k, d
    if dmax > eps:
        return rdp(pts[: i + 1], eps)[:-1] + rdp(pts[i:], eps)
    return [pts[0], pts[-1]]

paths = []
for d in data["districts"]:
    for poly in d["geom"]:
        full = [local(*c) for c in poly[0]]
        # closed ring: split at the point farthest from the start, simplify both halves
        k = max(range(len(full)), key=lambda q: math.hypot(full[q][0] - full[0][0], full[q][1] - full[0][1]))
        ring = rdp(full[: k + 1], 1.2)[:-1] + rdp(full[k:], 1.2)
        if len(ring) >= 3:
            paths.append("M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in ring) + "Z")
map_svg = (f'<img id="dtbase" src="__MAPSRC__" alt="Street map of Dortmund (OpenStreetMap)" style="position:absolute;left:{ox}px;top:{oy}px;width:{W}px;height:{H}px;object-fit:cover;border-radius:8px">\n'
           f'<svg id="dtmap" aria-label="Dortmund city districts" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'style="position:absolute;left:{ox}px;top:{oy}px;width:{W}px;height:{H}px">'
           f'<path d="{"".join(paths)}" fill="#36B3C7" fill-opacity="0.06" stroke="#36B3C7" stroke-opacity="0.35" stroke-width="1" stroke-linejoin="round"/></svg>\n'
           f'<p style="position:absolute;left:{ox + W - 420}px;top:{oy + H + 8}px;width:420px;text-align:right;font-size:24px;color:#8C9DAC">© OpenStreetMap contributors</p>')

# honeycomb coverage for slide B: every demand hexagon within reach of a station
HR = data["meta"]["hex_r_km"]
KXc, KYc = 111.32 * math.cos(math.radians(51.51)), 110.57
def hav(a, b, c, d):
    x = math.sin(math.radians(c - a) / 2) ** 2 + math.cos(math.radians(a)) * math.cos(math.radians(c)) * math.sin(math.radians(d - b) / 2) ** 2
    return 12742 * math.asin(math.sqrt(x))
one, two = [], []
for lat, lon, pop, d in data["cells"]:
    n = sum(1 for st in base["st"] if hav(lat, lon, st["lat"], st["lon"]) <= base["r"])
    if not n:
        continue
    pts = [local(lon + HR * math.cos(math.radians(a)) / KXc, lat + HR * math.sin(math.radians(a)) / KYc) for a in (30, 90, 150, 210, 270, 330)]
    (two if n > 1 else one).append("M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + "Z")
rings_svg = (f'<svg aria-label="Honeycomb coverage of the {len(base["st"])} stations" width="{W}" height="{H}" viewBox="0 0 {W} {H}" data-build-in="fade" '
             f'style="position:absolute;left:{ox:.0f}px;top:{oy:.0f}px;width:{W}px;height:{H}px">'
             f'<path d="{"".join(one)}" fill="#36B3C7" fill-opacity="0.22" stroke="#0E1620" stroke-opacity="0.6" stroke-width="1"/>'
             f'<path d="{"".join(two)}" fill="#36B3C7" fill-opacity="0.38" stroke="#0E1620" stroke-opacity="0.6" stroke-width="1"/>'
             + "".join(f'<circle cx="{local(st["lon"], st["lat"])[0]:.0f}" cy="{local(st["lon"], st["lat"])[1]:.0f}" r="{base["r"] * scale_km:.0f}" fill="none" stroke="#E4ECF2" stroke-opacity="0.45" stroke-width="1.5"/>' for st in base["st"])
             + '</svg>')

D = 44  # drone size px
def drone(i, x, y, rot, color):
    return (f'<svg id="drone{i}" aria-label="Drone" width="{D}" height="{D}" viewBox="0 0 44 44" '
            f'style="position:absolute;left:{x - D / 2:.0f}px;top:{y - D / 2:.0f}px;width:{D}px;height:{D}px;transform:rotate({rot}deg)">'
            f'<path d="M10 10L34 34M34 10L10 34" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>'
            f'<circle cx="10" cy="10" r="7" fill="none" stroke="{color}" stroke-width="2.5"/><circle cx="34" cy="10" r="7" fill="none" stroke="{color}" stroke-width="2.5"/>'
            f'<circle cx="10" cy="34" r="7" fill="none" stroke="{color}" stroke-width="2.5"/><circle cx="34" cy="34" r="7" fill="none" stroke="{color}" stroke-width="2.5"/>'
            f'<rect x="16" y="16" width="12" height="12" rx="3" fill="{color}"/></svg>')

rnd = random.Random(7)
scattered, organized = [], []
for i, s in enumerate(base["st"]):
    lx, ly = local(s["lon"], s["lat"])
    organized.append(drone(i, ox + lx, oy + ly, 0, "#F0553C"))
    # scattered: anywhere over the map area and the empty band left of it, random tilt
    sx = rnd.uniform(MX - 40, MX + MW - 30)
    sy = rnd.uniform(MY + 10, MY + MH - 10)
    scattered.append(drone(i, sx, sy, rnd.choice([-35, -20, -10, 12, 25, 40]), "#F0553C"))

TXT = {
    "en": dict(eyebrow="Team Pilots · DO-Data-Hackathon 2026",
               a_title="Today: drones everywhere, no network",
               a_body="Every agency buys its own drones. Different makers, no shared control, no plan for who is closest.",
               b_title="Air Shield: 27 stations, one network",
               b_body="The optimizer puts every drone where it reaches the most people within 4 minutes, 1 km apart, all controlled from one centre.",
               names="[Team member names]",
               a_note="We are Team Pilots. Today emergency drones in Dortmund are scattered: each agency has its own, no shared control and nobody knows which one is closest. Press next.",
               b_note="Air Shield organises them: 27 docked stations chosen by our optimizer from open data, at least 1 km apart, all run from the Morpheus control centre. Each circle is what one station reaches within four minutes; the honeycomb shows the result per area, darker cells are covered by two stations."),
    "de": dict(eyebrow="Team Pilots · DO-Data-Hackathon 2026",
               a_title="Heute: Drohnen überall, kein Netz",
               a_body="Jede Behörde kauft eigene Drohnen. Verschiedene Hersteller, keine gemeinsame Steuerung, kein Plan, wer am nächsten ist.",
               b_title="Air Shield: 27 Stationen, ein Netz",
               b_body="Der Optimierer setzt jede Drohne dorthin, wo sie in 4 Minuten die meisten Menschen erreicht, mit 1 km Abstand, gesteuert aus einem Leitstand.",
               names="[Namen der Teammitglieder]",
               a_note="Wir sind Team Pilots. Heute sind Einsatzdrohnen in Dortmund verstreut: jede Behörde hat eigene, es gibt keine gemeinsame Steuerung und niemand weiß, welche am nächsten ist. Weiter.",
               b_note="Air Shield ordnet sie: 27 Dock-Stationen, von unserem Optimierer aus Open Data gewählt, mindestens 1 km auseinander, gesteuert aus dem Morpheus-Leitstand. Die Waben zeigen jedes Gebiet, das eine Drohne in vier Minuten erreicht; dunklere Waben sind von zwei Stationen abgedeckt."),
}

def slide(sid, t, title, body, drones, extra, note, transition):
    head = (f'<p style="position:absolute;left:128px;top:128px;width:560px;font-family:\'Barlow Condensed\', Arial, sans-serif;font-size:28px;font-weight:600;letter-spacing:5px;text-transform:uppercase;color:#F0553C">{t["eyebrow"]}</p>'
            f'<h2 style="position:absolute;left:128px;top:200px;width:560px;font-family:\'Barlow Condensed\', Arial, sans-serif;font-size:80px;font-weight:700;line-height:1;text-transform:uppercase;color:#E4ECF2">{title}</h2>'
            f'<p style="position:absolute;left:128px;top:560px;width:540px;font-size:30px;line-height:1.4;color:#BFCDD8">{body}</p>'
            f'<p style="position:absolute;left:128px;bottom:64px;width:560px;font-size:24px;color:#8C9DAC">{t["names"]}</p>')
    return (f'<section id="{sid}" data-transition="{transition}" style="background:#0E1620;color:#E4ECF2;font-family:\'IBM Plex Sans\', Arial, sans-serif;padding:128px">\n'
            f'{map_svg}\n{extra}\n{head}\n' + "\n".join(drones) + f'\n<aside>{note}</aside>\n</section>\n')

for lang, folder in (("en", "deck_EN"),):
    t = TXT[lang]
    out = SCR / folder / "project" / "slides"
    (out / "team-a.html").write_text(slide("team-a", t, t["a_title"], t["a_body"], scattered, "", t["a_note"], "magic"), encoding="utf-8")
    (out / "team-b.html").write_text(slide("team-b", t, t["b_title"], t["b_body"], organized, rings_svg, t["b_note"], "fade"), encoding="utf-8")
    for f in ("team-a.html", "team-b.html"):
        print(folder, f, (out / f).stat().st_size // 1024, "KB")
print("map svg KB", len(map_svg) // 1024, "px/km", round(scale_km, 1), "crop", crop.size)
