# Gamma prompt — Dortmund Air Shield (English)

## Settings to choose in Gamma (Create › Paste in text)

| Setting | Choose |
|---|---|
| Mode | Presentation, 16:9 |
| Text handling | **Preserve** (keep our wording; do not let Gamma invent numbers) |
| Card split | By the `---` separators (19 cards) |
| Language | English |
| Theme | Dark theme (e.g. a navy/charcoal one); accent colour orange-red **#F0553C**, secondary cyan **#36B3C7** |
| Images | AI images, style “cinematic dark map, aerial city at night, drones, control room” — only on the cards that ask for one |
| Text density | Medium |

Then paste everything from the line `=== PROMPT START ===` to `=== PROMPT END ===` into the box. If you use **Gamma Agent** on an existing deck instead, paste the same block and add: “Rebuild this deck with exactly this content and order.”

---

=== PROMPT START ===

Create a 19-card investor-style pitch deck in English for a hackathon jury. Topic: “Dortmund Air Shield”, a city-wide drone network for emergency services (police, fire brigade, THW, city crisis unit), operated by Morpheus Logistik. Team name: Team Pilots.

Rules:
- Keep every number exactly as written. Do not add statistics, quotes, customer claims or logos that are not in this text.
- One idea per card. Short headlines (the headline is the message). Use tables as tables, not bullets.
- Visual style: dark control-room look, navy background, orange-red #F0553C as the single accent, cyan #36B3C7 for “good / covered”. Condensed bold headings, clean sans-serif body, monospace for big numbers.
- Big numbers as large stat blocks (cover, result, cost of sovereignty, cost per mission).
- Images only where an “Image:” line appears; never stock photos of people shaking hands.
- Follow the pitch structure: 1 Introduction, 2 Problem, 3 Product, 4 USP, 5 Team, 6 Customer interest, 7 Market, 8 Competition, 9 Business model, 10 Funding, 11 Call to action.
- Add speaker notes from the “Say:” lines.

---

# Dortmund Air Shield
The emergency-services drone network Dortmund doesn’t have yet: **4 minutes to anywhere in the city.**

Stats: **27** dock sites · **97.3%** of residents within 4 minutes · **2.2 min** average response · **€7.1M** investment

Team Pilots · Morpheus Logistik · DO-Data-Hackathon 2026 · Challenge 01

Image: dark night map of Dortmund from above with a glowing orange network of points.
Say: We plan one drone network for every emergency service in Dortmund. Three numbers: 27 sites, 2.2 minutes, 7.1 million euros.

---

# Today: drones everywhere, no network
Every agency buys its own drones. Different makers, no shared control, no plan for who is closest.

Image: dark map of Dortmund with about 27 orange quadcopter drones scattered randomly above it, tilted, no structure.
Say: When a fire breaks out in Scharnhorst, nobody knows which drone is closest.

---

# Seven questions in the brief, one answer each

| Problem | Our solution |
|---|---|
| Missions & shared fleet | 9 mission types with priority P1–P3; dock network for first response, special drones for the rest |
| European market | Comparison of EU/EEA/CH systems; mixed scenario only as a benchmark |
| Fleet & sites | Optimizer picks 27 of 48 emergency-service sites, docks sized to load |
| Open data & site model | 62 districts, 612,065 residents, honeycomb grid, transparent criteria |
| Law & airspace | Morpheus as technical operator; sovereign powers stay with the agencies |
| Ground risk & environment | Hospitals, airport vicinity and emergency landing areas in the model |
| Control, maintenance, cost | 24/7 remote pilots, two maintenance hubs, 5-year TCO, cost sharing |
| Bonus: dynamic model | Live recalculation for budget, missions, station failure and saved scenarios |

---

# Air Shield: 27 stations, one network
The optimizer puts every drone where it reaches the most people within 4 minutes, at least 1 km apart, all controlled from one centre.

Image: the same dark map of Dortmund, now 27 orange drones neatly on their stations, each with a soft cyan coverage circle.
Say: We are Team Pilots. Air Shield turns scattered drones into one network.

---

# Everything from the city’s open data
- **612,065** residents (2023) in 62 statistical districts
- **769** hexagons (0.36 km² each) as demand points
- **48** candidate sites: fire stations, volunteer fire brigades, police stations
- **18** hospitals as sensitive facilities
- **8** hotspots: stadium, central station, Westfalenhallen, port, airport, Phoenix-See, TU, Westfalenpark
- Dortmund airport vicinity and control zone as constraints

Sources: open-data.dortmund.de, OpenStreetMap, dipul.de

---

# From map to network in five steps
1. **Demand** – residents per cell plus extra weight for hotspots
2. **Candidates** – 48 agency sites with power and access control
3. **Reach** – launch + flight time ≤ target time
4. **Sites** – maximal covering model with backup coverage, under budget, stations ≥ 1 km apart
5. **Fleet** – docks per site sized for peak load (Erlang-B)

Re-plans in about 50 ms in the browser.
Show as a five-step horizontal process.

---

# 97.3% of residents reached within 4 minutes
Budget €9M · target 4 min · 8,000 missions a year

Stats: **2.2 min** average response · **74.7%** covered by two stations · **27 sites · 34 docks** · 12 volunteer fire brigades, 5 fire stations, 10 police stations

System chosen by the optimizer: Nokia Drone Networks (Finland), effective radius 2.7 km.
Say: Here we switch to the live planner for 60 seconds.

---

# Worst station failure: −4.6%, re-planned back to 97%

| Target time | Sites | Coverage |
|---|---|---|
| 3 min | 31 | 84.9% |
| **4 min** | **27** | **97.3%** |
| 5 min | 22 | 99.1% |
| 6 min | 18 | 99.8% |

| Budget | Sites | Coverage |
|---|---|---|
| €4M | 6 | 57.5% |
| €6M | 19 | 95.1% |
| **€9M** | **27** | **97.3%** |
| €12M | 27 | 97.3% |

Every variant can be saved, copied and compared as a scenario. Above about €7M more budget adds almost nothing.

---

# From emergency call to live video in 2.2 minutes
Three columns:
- **Control centre:** alert via interface · automatic assignment to the fastest free station · remote pilot, live video to the requester · 2 seats 24/7 = 11 staff
- **Maintenance:** two hubs (fire station 2 north, 4 south) · spare drone and parts per hub · on-site swap under 60 min
- **Redundancy:** overflow to the neighbour station · 75% of the area doubly covered · link loss: return home or emergency landing site

---

# The agencies keep authority, Morpheus flies

| Topic | Risk | Measure | Level |
|---|---|---|---|
| Sovereign powers | No official acts by private firms | Morpheus only a technical provider | Medium |
| § 21k LuftVO | Agency exemption not transferable | Specific category: SORA + LBA | High |
| BVLOS | SAIL II–III over housing | Parachute, geofencing, detect-and-avoid | High |
| Dortmund airport | Control zone, 2 sites nearby | Coordination with DFS and airport | Medium |
| UAS geozones | Hospitals, nature, industry | Consent per geozone (dipul.de) | Medium |
| Data protection | Footage of bystanders | Purpose limits, deletion, EU hosting | Medium |

No blanket exemption assumed.

---

# What makes it different
Four cards:
- **Existing sites** – all 27 stations on fire and police property: power, access control, staff already there
- **Live re-planning** – open data in, network out; budget, failures and scenarios re-plan in milliseconds
- **EU, with a price tag** – tender-compliant hardware; sovereignty costs €2.48 per resident per year
- **One network for all** – police, fire brigade, THW and city share one fleet, one control centre, one priority rule

---

# Team Pilots: data, operations, delivery

| Name | Role | Relevant experience |
|---|---|---|
| [Name] | Data & optimization | [one line] |
| [Name] | Product & demo | [one line] |
| [Name] | Operations & law | [one line] |
| [Name] | Business & pitch | [one line] |

**Built in 24 hours:** open-data pipeline, optimizer, live planner in German and English, scenario management, this deck.
**What connects us:** [one sentence]

---

# One shared fleet covers three in four missions

| Mission | Users | Priority | Platform |
|---|---|---|---|
| Fire / smoke | Fire brigade | P1 | Dock network |
| Missing-person search | Police, fire brigade | P1 | Dock network + VTOL |
| Hazmat / CBRN | Fire brigade, THW | P1 | Special drone |
| Collapse / indoor | Fire brigade, THW | P1 | Special drone |
| Traffic accident | Police | P2 | Dock network |
| Major event | Police | P2 | Planned, dock network |
| Flood / heavy rain | THW, civil protection | P2 | VTOL |
| Damage mapping | THW, city | P3 | VTOL |
| Crisis management | City of Dortmund | P3 | Dock network |

---

# Four customers, one need: eyes on scene first

| Customer | Problem today | What Air Shield gives them |
|---|---|---|
| Fire brigade | Crews arrive without a view from above | Thermal live image before the first engine |
| Police | Searches need fast overview | Drone on scene in 2.2 min on average |
| THW / civil protection | Floods need large-area maps | VTOL mapping on request |
| City crisis unit | No shared picture across agencies | One control centre, one live view |

**Validation status:** not yet tested with these customers. Next: interviews with Feuerwehr Dortmund, Polizeipräsidium Dortmund and THW, then a three-station pilot.

---

# Drone-in-a-box: three European systems compared

| Dock system | Origin | Radius | Flight time | Price* | Status |
|---|---|---|---|---|---|
| Nokia Drone Networks | FI | 5 km | 35 min | €150k | EU · selected |
| Azur Drones Skeyetech | FR | 4 km | 25 min | €160k | EU |
| Avy Aera + Dock (VTOL) | NL | 15 km | 70 min | €140k | EU · long range |
| Skydio X10 + Dock | US | 6 km | 40 min | €90k | Benchmark only |
| Percepto Air Max | IL | 5 km | 40 min | €140k | Benchmark only |
| DJI Dock 3 + M4TD | CN | 8 km | 54 min | €32k | Benchmark only |

The same engine plans any drone network: next, medical deliveries between Dortmund’s 18 hospitals; later, other cities in the Ruhr region.
*Estimates; verify before any tender.

---

# The alternatives today

| Alternative | Strength | Weakness |
|---|---|---|
| Each agency’s own drones | Own control | Duplicate cost, no shared view, pilot must drive out |
| Police helicopter | Large area, long endurance | Expensive per flight hour, not for every alert |
| Vehicle teams with hand drones | Flexible, cheap | Drive time before the first image |
| Docks with non-EU hardware | €10.6M vs €18.2M TCO | Not allowed under the tender, data sovereignty |
| **Air Shield** | **Automatic, 2.2 min, shared, EU** | **Needs BVLOS permits and a joint contract** |

---

# The cost of sovereignty: +€7.6M over five years
Big number: **+€7.6M** = **€2.48 per resident per year**

- EU only (Nokia, FI): 5-year TCO €18.2M · 97.3% coverage
- Mixed (DJI, CN): 5-year TCO €10.6M · 97.5% coverage — not allowed under the tender

Use the accent colour as the background of this card.

---

# €455 per mission, shared by four partners

| Investment | € |
|---|---|
| 34 docks incl. drone | 5.10M |
| Prepare 27 sites | 0.81M |
| Special drones | 0.61M |
| Control centre, DFS coordination | 0.53M |
| **Total** | **7.05M** |

| Partner | Share | € a year |
|---|---|---|
| Dortmund Fire Brigade | 42% | 1.53M |
| NRW Police | 36% | 1.31M |
| City crisis unit | 12% | 0.44M |
| THW / civil protection | 10% | 0.36M |
| **Total** | **100%** | **3.64M** |

Drone-as-a-service: Morpheus pre-finances and operates; partners pay 60% availability fee, 40% per mission. Operations €2.23M a year, 5-year TCO €18.2M.

---

# Three steps to a city-wide network
Timeline:
- **2027 H1 – Pilot:** 3 stations in the city centre, SORA and permit, dispatch link
- **2027 H2 – Scale-up:** 12 stations, routine BVLOS, maintenance hub north
- **2028 – City-wide:** 27 stations, 97% within 4 minutes, hub south
- **From 2029 – Region:** same model for neighbouring Ruhr cities

**Our ask:** anonymised dispatch data to calibrate demand, and the Dortmund Fire Brigade as pilot partner.

Closing line, large: **Four minutes to anywhere in Dortmund.**

=== PROMPT END ===
