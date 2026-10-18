# Air Shield Planner — how to read it

Link: https://claude.ai/artifact/8cDW4CvauKbHW9xBXpFVLK

The page has three columns (controls · map · results) and analysis sections below.
Everything recalculates within about 50 ms when you change anything.

---

## 1. Header

| Element | What it does |
|---|---|
| **EU / EEA / CH only** | Only drones and docks made in the EU, EEA or Switzerland (what the tender allows). Default. |
| **Mixed (EU + non-EU)** | Also allows US, Israeli and Chinese systems. Only a benchmark: shows what the EU rule costs. |

---

## 2. Left column — controls

### Scenario
| Element | What it does |
|---|---|
| **Active scenario** | Switch between saved scenarios. The line below the dropdown explains the active one. |
| **Name** | Rename the active scenario by typing. |
| **New** | New scenario with default settings. |
| **Copy** | Duplicate the active scenario to try a variant. |
| **Delete** | Asks “Confirm delete?” — click again within 3 s. |

Every slider change is saved into the active scenario (in your browser only; teammates don’t see your scenarios).

**Preset scenarios (in pitch order):**

| Scenario | Story | Result |
|---|---|---|
| ★ Recommended: 4 min · €9M | Our proposal | 27 sites · 97.3% · €7.1M · €455/mission |
| Pilot 2027: €2.5M | Start small, prove operations | 3 sites · 36% |
| Phase 1: €4M | First expansion | 6 sites · 58% |
| Lean city-wide: €6M | Tight budget | 19 sites · 95% · less backup |
| Faster: 3-minute response | Stricter target | 31 sites · only 85% (reach limit) |
| Relaxed: 5-minute response | Looser target | 22 sites · 99% · almost all doubly covered |
| Major incident year: 20,000 missions | 2.5× the alerts | same sites, 48 docks · €224/mission |
| No sites near the airport | If DFS says no | 26 sites · 94% |
| Benchmark: mixed suppliers | Not tender-compliant | DJI · €2.6M investment · shows the cost of sovereignty |

### Parameters
| Slider | Meaning | Effect |
|---|---|---|
| **Capital budget** | Maximum investment (docks, site preparation, special drones, control centre). | The optimizer never plans above it. Above about €7M it stops binding, because further sites add too little. |
| **Target response time** | Alert → drone on scene. | The strongest lever. Shorter = smaller reach circle = more sites needed. |
| **Missions per year** | Expected alerts in the whole city. | Changes the number of docks per site (peak load) and the cost per mission; not where the sites are. |
| **Dock system** | “Automatic” tests every allowed hover-capable system and keeps the best coverage (cheaper one if within 0.5 %). Or pick one manually, e.g. the VTOL Avy Aera. | Speed, launch time and range set the reach circle; price sets how many sites fit the budget. |
| System card | Shows the chosen system: origin, type, rain rating, speed, flight time, range, launch time, and the **effective radius at target time** (= the reach circle on the map). | — |

### Weights & assumptions (click to open)
| Slider | Meaning |
|---|---|
| **Weight of backup coverage (β)** | How much a second station covering the same area is worth. 0 = only first coverage counts (fewer sites, no redundancy); 1 = backup counts as much as first coverage. Default 0.5. |
| **Minimum gain per station** | A site is only added if it brings at least this share of extra value (default 0.4 %). Stops the optimizer from spending money on sites that add almost nothing. |
| **Peak-load factor** | How much busier the busiest hour is than average (default ×3). Drives docks per site. |
| **Max. rejection rate per station** | Share of alerts at peak that may overflow to the neighbouring station because all docks are busy (default 10 %). Lower = more docks. |
| **Minimum distance between stations** | Default 1 km. Two sites closer than this would share power, weather and access, so they don’t count as real redundancy. |
| **Allow sites near the airport** | On = sites within 2.5 km of Dortmund airport are allowed but need DFS coordination (+€40k each, flagged). Off = excluded. |

### Buttons
| Button | What it does |
|---|---|
| **Re-plan with failures** | Takes the stations you marked as failed, bans them, and optimizes again with the remaining candidates. |
| **Reset failures** | Clears failed and banned stations. |

---

## 3. Middle — the map

### Map buttons (top left)
| Button | Shows |
|---|---|
| **Coverage** (default) | Each hexagon coloured by how many stations reach it within the target time. |
| **Response time** | Each hexagon coloured by the fastest arrival time: cyan = fast, orange-red = at the target time, amber = beyond. |
| **Population** | Residents per hexagon (light = few, dark blue = many). Use it to explain where demand is. |
| **Street map** | Turns the OpenStreetMap background on/off. |

### What you see
| Element | How to read it |
|---|---|
| **Hexagons (honeycomb)** | The city split into 769 hexagons of 0.36 km² each. Each is one demand point with its residents (spread evenly per district) plus extra weight at hotspots (stadium, central station, Westfalenhallen, port, airport, Phoenix-See, TU, Westfalenpark). |
| Dark teal hexagon | Reached by **two or more** stations within target time (redundant — survives a station failure). |
| Light cyan hexagon | Reached by **one** station. |
| Amber hexagon | **Not covered** within the target time. |
| **Thin circles** | The **reach** of each station: how far its drone gets within the target time (launch time + flight at cruise speed, with a 1.15 detour factor, capped by the drone’s range). Dashed red = that station has failed. |
| **Orange diamonds** | Selected dock stations. A label “×2” means two docks at that site (needed for peak load). |
| Small grey dots | Candidate sites the optimizer did **not** choose. |
| Small grey crosses | Hospitals (sensitive facilities). |
| **Amber dashed circle / filled circle** | Dortmund airport: schematic control zone (6 km) and near zone (2.5 km). |
| District outlines | The 62 statistical districts from open data. |

Circles vs hexagons: the circle is the *input* (where one drone can get to); the hexagon colour is the *result* (how many stations reach that area).

### Interactions
| Action | Result |
|---|---|
| Hover a hexagon | District, residents, response time, number of stations in reach. |
| Hover a station | Name, type, docks, missions per year; its hexagons get an orange outline. |
| **Click a station** | Simulates a failure: it turns red, its circle becomes dashed, coverage and KPIs update. Click again to restore. |
| Scroll / drag | Zoom and pan. |

---

## 4. Right column — result

### KPI tiles (coloured top line: green = good, amber = watch, red = problem)
| KPI | Meaning |
|---|---|
| **Population within target time** | Share of 612,065 residents reached in time (with current failures). Green ≥ 90 %. |
| **Avg. response time** | Average arrival time for covered residents. |
| **Redundantly covered** | Share of residents reached by ≥ 2 stations. Green ≥ 60 %. |
| **Sites · docks** | Active stations · total docks (some sites have 2+). |
| **Investment** | Docks + site preparation + airport coordination + special drones + control centre. Red if over budget. |
| **Operations per year** | Maintenance, insurance, remote pilots, software, special drones. |
| **Cost per mission** | (Investment ÷ 5 years + operations) ÷ missions per year. |
| **Worst single failure** | Coverage lost if the most critical station fails (computed for every station). |

### Below the tiles
| Element | Meaning |
|---|---|
| Alerts (amber boxes) | Most critical site; failed stations and coverage drop; sites needing airport coordination. |
| **Population by coverage** bar | Dark = redundant, cyan = single, amber = not covered (with resident counts). |
| **Stations list** | All selected sites, sorted by missions per year: name, docks (e.g. 2×), missions. Click a row = same as clicking the station on the map. “DFS” tag = near the airport. |

---

## 5. Sections below the map

| Section | How to read it |
|---|---|
| **Scenario comparison** | One row per saved scenario: suppliers, system, budget, target, missions, sites, docks, coverage, redundancy, avg. time, investment, 5-year TCO, € per mission. Green = best coverage / lowest TCO. Click a row to open it. |
| **Cost of sovereignty** | Optimizes EU-only and Mixed with identical settings. Big number = extra 5-year cost of EU-only; text = coverage difference and cost per resident per year. |
| **Fleet & costs** | Fleet table (dock drones, special drones, control seats) + investment and yearly cost breakdown + 5-year TCO. |
| **Cost sharing between agencies** | Yearly cost split: fire brigade 42 %, police 36 %, city 12 %, THW 10 % (assumption, from the mission mix). |
| **Mission profiles** | The 9 mission types, users, sensors, priority (P1 life, P2 situation, P3 documentation) and which platform handles them. |
| **Method & assumptions** | How demand, candidates, coverage, optimization, fleet sizing, control centre and airspace are modelled; data sources. |

---

## 6. How the optimizer decides (one paragraph)

For every candidate site it lists the hexagons a drone reaches within the target time. It then adds sites one by one, always taking the one that brings the most value per euro (a hexagon covered for the first time counts fully, a second time counts β, a third time nothing), until the budget is used or the next site adds less than the minimum gain. Sites closer than the minimum distance are not allowed together. Then it tries swapping each chosen site for each unused one and keeps any swap that improves the result. Finally it sizes docks per site with Erlang-B for the peak hour. Result: a very good, not provably optimal, plan.

---

## 7. 60-second demo script

1. Point at the map: “Every hexagon is 0.36 km² of Dortmund; teal means two stations reach it in four minutes, the circles show each station’s reach.”
2. Click **Feuer- und Rettungswache 6 – Scharnhorst** → coverage drops 4.6 % → **Re-plan with failures** → back to about 97 %.
3. **Reset failures**, switch scenario to **Lean city-wide: €6M** → 19 stations, about 95%; then **Faster: 3-minute response** → only 85%: speed has a physical limit.
4. Scroll to **Cost of sovereignty**: “EU-only costs €7.6M more over five years, €2.48 per resident per year.”

## 8. Limits to say honestly
- Drone prices and specs are estimates; verify before a tender.
- Residents are spread evenly within each district; real dispatch data would be better.
- Airport zone is schematic; real geozones from dipul.de.
- Flight is straight line × 1.15; no weather or night restrictions.
- The optimizer is a heuristic: very good, not proven optimal.
