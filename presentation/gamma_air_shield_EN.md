# Dortmund Air Shield

The emergency-services drone network Dortmund doesn’t have yet: **4 minutes to anywhere in the city.**

- 27 dock sites
- 97.3% of residents reached within 4 minutes
- 2.2 min average response time
- €7.1M investment

Team Pilots · Morpheus Logistik · DO-Data-Hackathon 2026 · Challenge 01

---

# Today: drones everywhere, no network

Every agency buys its own drones. Different makers, no shared control, no plan for who is closest.

Image idea: dark map of Dortmund with about 27 orange quadcopter drones scattered randomly above it, tilted at different angles, no structure.

---

# Seven questions in the brief, one answer each

| Problem | Our solution |
|---|---|
| 01 Missions & shared fleet | 9 mission types with priority P1–P3; dock network for first response, special drones for the rest |
| 02 European market | Comparison of EU/EEA/CH systems; mixed scenario only as a benchmark |
| 03 Fleet & sites | Optimizer picks 27 of 48 emergency-service sites, docks sized to load |
| 04 Open data & site model | 62 districts, 612,065 residents, honeycomb grid, transparent criteria |
| 05 Law & airspace | Morpheus as technical operator, sovereign powers stay with the agencies |
| 06 Ground risk & environment | Hospitals, airport vicinity and emergency landing areas in the model |
| 07 Control, maintenance, cost | 24/7 remote pilots, two maintenance hubs, 5-year TCO, cost sharing |
| Bonus: dynamic model | Live recalculation for budget, mission count, station failure and saved scenarios |

---

# Air Shield: 27 stations, one network

The optimizer puts every drone where it reaches the most people within 4 minutes, at least 1 km apart, all controlled from one centre.

Image idea: the same dark map of Dortmund, now with 27 orange drones sitting neatly on their stations, each with a soft cyan coverage circle around it.

---

# Everything from the city’s open data portal

- **612,065** residents (2023) in 62 statistical districts
- **769** hexagons (0.36 km² each) as demand points
- **48** candidate sites: fire stations, volunteer fire brigades, police stations
- **18** hospitals as sensitive facilities
- **8** hotspots: stadium, central station, Westfalenhallen, port, airport, Phoenix-See, TU, Westfalenpark
- **Dortmund airport** vicinity and control zone as constraints

Sources: open-data.dortmund.de, OpenStreetMap, dipul.de

---

# From map to network in five steps

1. **Demand** – residents per cell plus extra weight for hotspots
2. **Candidates** – 48 agency sites with power and access control
3. **Reach** – launch + flight time ≤ target time, detour factor 1.15
4. **Sites** – maximal covering model with backup coverage under budget, stations at least 1 km apart
5. **Fleet** – docks per site via Erlang-B for peak load

Greedy by gain per euro, then a swap heuristic. Re-plans in about 50 ms in the browser.

---

# 97.3% of residents reached within 4 minutes

Budget €9M · target 4 min · 8,000 missions a year

- **2.2 min** average response time
- **74.7%** reachable from two stations (redundant)
- **27 sites · 34 docks**
- Sites: 12 volunteer fire brigades · 5 fire stations · 10 police stations
- System chosen by the optimizer: Nokia Drone Networks (FI), effective radius 2.7 km

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

- Most critical site: fire station 6 Scharnhorst (−4.6% if it fails; re-planning restores 97.1%)
- Every variant can be saved, copied and compared as a scenario in the planner
- Above about €7M the budget no longer binds: extra sites add under 0.4% coverage each

---

# From emergency call to live video in 2.2 minutes

**Control centre**
- Alert from the agency dispatch via interface
- Automatic assignment to the fastest free station
- Remote pilot takes over, live video to the requester
- 2 seats 24/7 = 11 full-time staff

**Maintenance**
- Two hubs: fire station 2 (north) and 4 (south)
- One spare drone and parts per hub
- On-site swap in under 60 minutes

**Redundancy**
- Busy station: overflow to the neighbour
- Station failure: 75% of the area doubly covered
- Link loss: return home or emergency landing site

---

# The agencies keep authority, Morpheus flies

| Topic | Risk | Measure | Level |
|---|---|---|---|
| Sovereign powers | No official acts by private firms | Morpheus only a technical provider | Medium |
| § 21k LuftVO | Agency exemption not transferable | Specific category: SORA + LBA | High |
| BVLOS | SAIL II–III over housing | Parachute, geofencing, detect-and-avoid | High |
| Dortmund airport | CTR, 2 sites in the vicinity | Coordination with DFS and airport | Medium |
| UAS geozones | Hospitals, nature, industry | Consent per geozone (dipul.de) | Medium |
| Data protection | Footage of bystanders | Purpose limits, deletion, EU hosting | Medium |

No blanket exemption assumed; relief is checked per mission type.

---

# What makes it different

- **Existing sites:** all 27 stations sit on fire and police property; power, access control and staff already there
- **Live re-planning:** open data in, network out; budget, failures and scenarios re-plan in milliseconds
- **EU, with a price tag:** tender-compliant hardware, and we show what sovereignty costs: €2.48 per resident per year
- **One network for all:** police, fire brigade, THW and city share one fleet, one control centre and one priority rule

---

# Team Pilots: data, operations, delivery

| Name | Role | Relevant experience |
|---|---|---|
| [Name] | Data & optimization | [one line] |
| [Name] | Product & demo | [one line] |
| [Name] | Operations & law | [one line] |
| [Name] | Business & pitch | [one line] |

**Built in 24 hours:** open-data pipeline, optimizer, live planner in German and English, scenario management, this deck.

**What connects us:** [why this problem matters to us, one sentence]

---

# One shared fleet covers three in four missions

| Mission | Users | Priority | Platform |
|---|---|---|---|
| Fire / smoke | Fire brigade | P1 | Dock network |
| Missing-person search | Police, fire brigade | P1 | Dock network + VTOL |
| Hazmat / CBRN | Fire brigade, THW | P1 | Special drone |
| Collapse / indoor | Fire brigade, THW | P1 | Special drone |
| Traffic accident / overview | Police | P2 | Dock network |
| Major event | Police | P2 | Planned, dock network |
| Flood / heavy rain | THW, civil protection | P2 | VTOL |
| Damage mapping | THW, city | P3 | VTOL |
| Crisis management | City of Dortmund | P3 | Dock network |

---

# Four customers, one shared need: eyes on scene first

| Customer | Their problem today | What Air Shield gives them |
|---|---|---|
| Fire brigade | Crews arrive without a view from above | Thermal live image before the first engine |
| Police | Searches and incidents need fast overview | Drone on scene in 2.2 min on average |
| THW / civil protection | Floods and damage need large-area maps | VTOL mapping on request |
| City crisis unit | No shared picture across agencies | One control centre, one live view |

**Validation status:** not yet tested with these customers. Next step: interviews with Feuerwehr Dortmund, Polizeipräsidium Dortmund and THW, then a three-station pilot.

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

Plus European special drones: Quantum-Systems Vector (DE), Parrot ANAFI USA (FR), Flyability Elios 3 (CH).

*Estimates from manufacturer data and market research; verify before any tender.

---

# The alternatives today

| Alternative | Strength | Weakness |
|---|---|---|
| Each agency’s own drones | Under their own control | Duplicate cost, no shared view, pilot must drive out |
| Police helicopter | Large area, long endurance | Expensive per flight hour, not for every alert |
| Vehicle teams with hand drones | Flexible, cheap hardware | Drive time before the first image |
| Docks with non-EU hardware | Cheaper: €10.6M vs €18.2M TCO | Not allowed under the tender, data sovereignty |
| **Air Shield** | **Automatic, 2.2 min, shared, EU** | **Needs BVLOS permits and a joint contract** |

---

# The cost of sovereignty: +€7.6M over five years

- **EU only** (Nokia, FI): 5-year TCO €18.2M · 97.3% coverage
- **Mixed** (DJI, CN): 5-year TCO €10.6M · 97.5% coverage (not allowed under the tender rules)
- Difference: **€2.48 per resident per year** for data sovereignty and a secure supply chain

---

# €455 per mission, shared by four partners

| Investment | € |
|---|---|
| 34 docks incl. drone | 5.10M |
| Prepare 27 sites | 0.81M |
| Special drones | 0.61M |
| Control centre, DFS coordination | 0.53M |
| **Total** | **7.05M** |

Operations €2.23M a year · 5-year TCO €18.2M

| Partner | Share | € a year |
|---|---|---|
| Dortmund Fire Brigade | 42% | 1.53M |
| NRW Police | 36% | 1.31M |
| City (crisis unit) | 12% | 0.44M |
| THW / civil protection | 10% | 0.36M |
| **Total** | **100%** | **3.64M** |

Business model: drone-as-a-service. Morpheus pre-finances and operates; partners pay a 60% base fee for availability and 40% per mission.

---

# Three steps to a city-wide network

- **2027 H1 – Pilot:** 3 stations in the city centre, SORA and operating permit, dispatch link
- **2027 H2 – Scale-up:** 12 stations, routine BVLOS, maintenance hub north
- **2028 – City-wide:** 27 stations, 97% within 4 minutes, second hub south
- **From 2029 – Region:** same model for neighbouring Ruhr cities

**Our ask:** anonymised dispatch history to calibrate demand, and the Dortmund Fire Brigade as pilot partner.

Four minutes to anywhere in Dortmund. Thank you.
