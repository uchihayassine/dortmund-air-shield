# Air Shield — calculation methods

How every number in the planner is computed, with a worked example from the **★ Recommended** scenario (EU only, €9M budget, 4-minute target, 8,000 missions a year).
The code lives in `app/planner.template.html` (section “optimizer”); `tools/export_csv.js` runs the same code and writes all results to `data/export/`.

---

## 0. Overview

```
open data ──► demand hexagons ──► reach per site ──► site selection (greedy + swap)
                                                        │
                    missions per year ──► fleet sizing (Erlang-B) ──► costs ──► KPIs
                                                        │
                                   robustness · scenarios · cost of sovereignty
```

| Step | Method | Main inputs | Output |
|---|---|---|---|
| 1 | Demand grid | Districts, population, hotspots | 769 weighted hexagons |
| 2 | Distances | Coordinates | 769 × 48 distance matrix |
| 3 | Reach & coverage | Target time, drone speed, launch time, range | Hexagons each site reaches |
| 4 | Site selection | Budget, β, minimum gain, spacing, airport rule | Chosen stations |
| 5 | Fleet sizing | Missions, peak factor, max. overflow | Docks per station |
| 6 | Costs | Prices and rates | Investment, operations, TCO, € per mission |
| 7 | KPIs | Coverage counts | Coverage %, redundancy %, average time |
| 8 | Robustness | Chosen stations | Worst single failure |
| 9 | Comparisons | Two full runs | Cost of sovereignty, scenarios |

---

## 1. Demand grid (honeycomb)

- Pointy-top hexagons with area **0.36 km²** (same as a 600 m square).
  Circumradius R = √(0.36 / (1.5·√3)) = **0.372 km**; column spacing √3·R = 0.645 km; row spacing 1.5·R = 0.558 km; every second row shifted half a column.
- A hexagon belongs to a district if its centre lies inside the district polygon (even-odd point-in-polygon test). Result: **769 hexagons**.
- **Population per hexagon** = district population ÷ number of hexagons in that district (even spread).
- **Weight per hexagon** = population + hotspot bonus (bonus added to the hexagon nearest each hotspot, e.g. stadium +20,000).
- Total population 612,065 (open data, 2023).

## 2. Distances

Haversine (great-circle) distance in km:

d = 12,742 · asin( √( sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2) ) )

Computed once for all 769 × 48 hexagon–site pairs and for all 48 × 48 site pairs (spacing rule).

## 3. Reach and coverage

Response time from site j to hexagon i:

t(i,j) = launch time + d(i,j) × 1.15 ÷ speed

(speed in km/min = m/s × 0.06; 1.15 = detour factor because drones don’t fly perfectly straight)

Hexagon i is **covered** by site j if t(i,j) ≤ target time **and** d(i,j) ≤ drone range. Equivalent reach radius:

r = min( range, (target − launch) × speed ÷ 1.15 )

**Worked example (Nokia, 4 min):** speed 16 m/s = 0.96 km/min, launch 45 s = 0.75 min.
r = (4 − 0.75) × 0.96 ÷ 1.15 = **2.71 km** (below the 5 km range, so time is the limit). This is the circle on the map.

## 4. Site selection (optimizer)

**Objective:** maximize Σᵢ wᵢ · v(nᵢ), where nᵢ = number of chosen sites covering hexagon i and the value of the *next* covering site is
v = 1 if nᵢ = 0 (first coverage), β if nᵢ = 1 (backup, β = 0.5), 0 if nᵢ ≥ 2.

**Constraints:**
- Total investment ≤ capital budget
- Distance between any two chosen sites ≥ minimum spacing (1 km)
- Airport-area sites (≤ 2.5 km from DTM) only if allowed; they cost +€40k
- Banned (failed) sites excluded
- Only EU/EEA/CH systems unless “mixed” is selected

**Algorithm:**
1. **Greedy:** repeat — for every allowed, unchosen site compute gain = Σ over its covered hexagons wᵢ·v(nᵢ); site cost = dock price + €30k (+ €40k airport). Pick the site with the highest gain ÷ cost that fits the remaining budget and the spacing rule. Stop when nothing fits or the best gain < minimum gain (0.4 % of total weight).
2. **Swap (1-opt):** for each chosen site, remove it (update nᵢ), then test every unchosen site in its place; keep the swap with the highest gain if it beats the removed site’s contribution and fits budget and spacing. Up to 3 passes. Gains are computed incrementally (only the hexagons of the two sites involved).
3. **Budget fit:** fleet sizing (step 5) may add docks. If total investment exceeds the budget, the site budget is reduced by the overshoot and steps 1–2 rerun (up to 8 times); last resort: drop the least-used site.
4. **Automatic system choice:** steps 1–3 run for every eligible hover-capable dock system; the plan with the highest coverage wins; if another is within 0.5 % coverage and has a lower 5-year TCO, that one wins.

Heuristic: fast (≈ 30–50 ms) and close to optimal, but not a proven optimum.

## 5. Fleet sizing (docks per site)

1. Each covered hexagon is assigned to its **fastest** station; a station’s demand share = its assigned weight ÷ total covered weight.
2. Missions per station = missions per year × covered share × station share.
3. Service time per mission h = (2 × average distance × 1.15 ÷ speed + 15 min on scene + recharge time) ÷ 60  [hours].
4. Peak-hour load (Erlang) a = missions per station ÷ 8,760 h × peak factor × h.
5. **Erlang-B** blocking with c docks: B(0) = 1, B(c) = a·B(c−1) ÷ (c + a·B(c−1)).
   Docks = smallest c with B(c) ≤ max. overflow (10 %). Blocked alerts go to the neighbouring station (backup coverage).

**Worked example (Polizeiwache Mitte, busiest station):** 857 missions a year, service time ≈ 52 min (≈ 2.4 min flying + 15 min on scene + 35 min recharge), peak ×3:
a = 857 ÷ 8,760 × 3 × 0.87 = **0.256**.
B(1) = 0.256 ÷ 1.256 = **20.4 %** > 10 % → not enough.
B(2) = 0.256 × 0.204 ÷ (2 + 0.256 × 0.204) = **2.5 %** ≤ 10 % → **2 docks** (“×2” on the map).

## 6. Control-centre staffing

- Simultaneous flights at peak ≈ Σ a over all stations.
- Seats = max(2, ⌈Σ a ÷ 3⌉) — one remote pilot supervises up to 3 automated flights; minimum 2 seats for redundancy.
- Staff = seats × 5.5 FTE (24/7 coverage incl. shifts, weekends, holidays, sickness).
- Recommended: Σ a < 6 → **2 seats = 11 FTE**.

## 7. Costs

**Investment (one-off)**
= docks × dock price + sites × €30k + airport sites × €40k + special drones + €450k control-centre integration

**Operations per year**
= docks × (system opex + €4.5k insurance) + seats × 5.5 × €82k + €220k software + 12 % × special-drone value

**5-year TCO** = investment + 5 × operations
**Annual cost** = investment ÷ 5 + operations
**Cost per mission** = annual cost ÷ missions per year
**Agency cost** = annual cost × share (42 / 36 / 12 / 10 %)

**Worked example (Recommended):**

| Item | Calculation | € |
|---|---|---|
| Docks | 34 × 150,000 | 5,100,000 |
| Site preparation | 27 × 30,000 | 810,000 |
| Airport coordination | 2 × 40,000 | 80,000 |
| Special drones | 2×180k + 8×14k + 1×140k | 612,000 |
| Control centre | 1 × 450,000 | 450,000 |
| **Investment** | | **7,052,000** |
| Dock opex | 34 × 26,000 | 884,000 |
| Insurance | 34 × 4,500 | 153,000 |
| Remote pilots | 2 × 5.5 × 82,000 | 902,000 |
| Software | | 220,000 |
| Special-drone upkeep | 12 % × 612,000 | 73,440 |
| **Operations / year** | | **2,232,440** |
| 5-year TCO | 7,052,000 + 5 × 2,232,440 | 18,214,200 |
| Annual cost | 7,052,000 ÷ 5 + 2,232,440 | 3,642,840 |
| Cost per mission | 3,642,840 ÷ 8,000 | **455** |

## 8. KPIs

| KPI | Formula |
|---|---|
| Population within target time | Σ population of covered hexagons ÷ 612,065 |
| Redundantly covered | Σ population of hexagons with nᵢ ≥ 2 ÷ 612,065 |
| Avg. response time | Σ (fastest time × weight) ÷ Σ weight, covered hexagons only |
| Sites · docks | Chosen sites · Σ docks |
| Worst single failure | max over stations of (coverage − coverage without that station), no re-planning |

Failures clicked in the map change the coverage KPIs immediately; costs stay those of the intact plan. “Re-plan with failures” bans the failed sites and reruns step 4.

## 9. Cost of sovereignty

Run the full optimization twice with identical settings: EU only and mixed (non-EU allowed).

Extra cost = TCO(EU) − TCO(mixed) = 18,214,200 − 10,630,300 = **€7.58M** over 5 years
Per resident per year = 7.58M ÷ 612,065 ÷ 5 = **€2.48**

## 10. Scenarios and sensitivity

- A scenario = one saved set of inputs; each is solved with steps 3–9 and cached by its parameters.
- `data/export/scenarios.csv` lists all presets with inputs and outputs.
- `data/export/sensitivity.csv` changes one input at a time from the recommended case.

---

## Exported CSV files (`data/export/`, UTF-8, comma-separated)

| File | Content |
|---|---|
| `cells.csv` | 769 hexagons: coordinates, district, population, weight, hotspot, stations in reach, best response time, covered/redundant (recommended plan) |
| `districts.csv` | 62 districts: population, hexagons, covered %, redundant %, average response time |
| `candidate_sites.csv` | 48 fire/police sites: type, coordinates, airport distance, selected, docks, missions, peak load |
| `hospitals.csv`, `hotspots.csv` | Context layers |
| `drone_systems.csv`, `special_drones.csv` | System catalogue with specs and prices (estimates) |
| `missions.csv`, `cost_split.csv` | Mission catalogue and agency split |
| `assumptions.csv` | Every input and constant with unit and status (sourced / estimate / choice) |
| `data_sources.csv` | Where each data item comes from |
| `recommended_costs.csv` | Line-by-line investment and operating costs |
| `scenarios.csv` | All preset scenarios: inputs and results |
| `cost_of_sovereignty.csv` | EU-only vs mixed |
| `sensitivity.csv` | One-at-a-time changes from the recommended case |
| `scenario_stations.csv` | Which stations (with docks and missions) each of the 9 scenarios picks |
| `reach_matrix.csv` | Every hexagon–site pair within reach in the recommended plan: distance and response time |
| `distance_matrix.csv` | All 769 × 48 hexagon–site distances (km) |
| `district_geometry.csv`, `hexagon_geometry.csv` | Shapes as WKT polygons (for QGIS, Power BI, Excel maps) |
| `raw_population_2023.csv`, `raw_feuerwehr.csv`, `raw_polizei.csv`, `raw_krankenhaus.csv` | Original open-data tables, unchanged |

Regenerate after any model change:
```bash
python tools/build_app.py
node tools/export_csv.js
python tools/export_raw_csv.py
```
