# Dortmund Air Shield (EN) — slide text and speaker notes

19 slides. Source: `presentation/deck_EN/project/`. Live deck: https://claude.ai/artifact/FJ9M2YcumqxRwVyPRG1sF1

---

## Part: 1 Introduction

### Slide 1 · `cover`

Morpheus Logistik · DO-Data-Hackathon 2026 · Challenge 01

# Dortmund Air Shield

One drone network for every emergency service in the city: 97% of residents reached within 4 minutes, with European hardware.

27

dock sites

2.2 min

avg. response time

€7.1M

investment

Team Pilots · 17 Oct 2026

> **Speaker notes:** We plan a city-wide drone network for police, fire brigade, THW and the city, run by Morpheus as a neutral operator. Three numbers up front: 27 sites, 2.2 minutes on average to the scene, 7.1 million euros of investment. Everything can be recalculated live in the Air Shield Planner.

---

## Part: 2 Problem

### Slide 2 · `team-a`

*[Image: Street map of Dortmund (OpenStreetMap)]*

© OpenStreetMap contributors

Team Pilots · DO-Data-Hackathon 2026

## Today: drones everywhere, no network

Every agency buys its own drones. Different makers, no shared control, no plan for who is closest.

[Team member names]

> **Speaker notes:** We are Team Pilots. Today emergency drones in Dortmund are scattered: each agency has its own, no shared control and nobody knows which one is closest. Press next.

### Slide 3 · `challenge`

The task

## Seven questions in the brief, one answer each

| Problem | Our solution |
|---|---|
| 01 Missions & shared fleet | 9 mission types with priority P1–P3; dock network for first response, special drones for the rest |
| 02 European market | Comparison of EU/EEA/CH systems; mixed scenario only as a benchmark |
| 03 Fleet & sites | Optimizer picks 27 of 48 emergency-service sites, docks sized to load |
| 04 Open data & site model | 62 districts, 612,065 residents, 600 m grid, transparent criteria |
| 05 Law & airspace | Morpheus as technical operator, sovereign powers stay with the agencies |
| 06 Ground risk & environment | Hospitals, airport vicinity and emergency landing areas in the model |
| 07 Control, maintenance, cost | 24/7 remote pilots, two maintenance hubs, 5-year TCO, cost sharing |
| Bonus Dynamic model | Live recalculation for budget, mission count, station failure and saved scenarios |

Source: Morpheus Logistik challenge briefing, DO-Data-Hackathon 2026

> **Speaker notes:** The brief sets seven topic blocks plus a bonus. Each row is one chapter of this talk and one part of the planner.

---

## Part: 3 Product: network, model, results, operations, law

### Slide 4 · `team-b`

*[Image: Street map of Dortmund (OpenStreetMap)]*

© OpenStreetMap contributors

Team Pilots · DO-Data-Hackathon 2026

## Air Shield: 27 stations, one network

The optimizer puts every drone where it reaches the most people within 4 minutes, 1 km apart, all controlled from one centre.

[Team member names]

> **Speaker notes:** Air Shield organises them: 27 docked stations chosen by our optimizer from open data, at least 1 km apart, all run from the Morpheus control centre. Each circle is what one station reaches within four minutes; the honeycomb shows the result per area, darker cells are covered by two stations.

### Slide 5 · `data`

Data

## Everything from the city’s open data portal

612,065

residents (2023) in 62 statistical districts

769

hexagons (0.36 km²) as demand points

48

candidates: fire stations, volunteer brigades, police

18

hospitals as sensitive facilities

8

hotspots: stadium, station, halls, port …

DTM

airport vicinity and control zone as constraints

Sources: open-data.dortmund.de (statistical districts, population 2023, fire brigade, police, hospitals); geozones: dipul.de

> **Speaker notes:** Why emergency-service sites as candidates: power, network, access control and staff are already there, and permits on the clients’ own grounds are simplest. Assumption: residents are spread evenly within a district. Real dispatch data would sharpen the model further.

### Slide 6 · `model`

Optimization model

## From map to network in five steps

1

**Demand**

Residents per cell plus extra weight for hotspots

2

**Candidates**

48 agency sites with power and access control

3

**Reach**

Launch + flight time ≤ target, detour factor 1.15

4

**Sites**

Maximal covering with backup coverage under budget

5

**Fleet**

Docks per site via Erlang-B for peak load

max Σ wᵢ · (first station + β · second station) s.t. Σ cost ≤ budget

Greedy by gain per euro, then a swap heuristic · runs in about 50 ms in the browser

> **Speaker notes:** The model is deliberately transparent. Each cell has a weight from residents and hotspots. A cell counts as covered if the drone gets there within the target time. The second-station term rewards redundancy: if one station fails, the area stays served. Because it runs in milliseconds in the browser, we can change any assumption live.

### Slide 7 · `result`

Result · budget €9M · target 4 min · 8,000 missions a year

97.3%

of residents can be reached by a drone within 4 minutes

2.2 min

avg. response time

74.7%

reachable from two stations

27 · 34

sites · docks

12 · 5 · 10

volunteer · fire · police sites

System chosen by the optimizer: Nokia Drone Networks (FI), effective radius 2.7 km · live in the Air Shield Planner

> **Speaker notes:** With the EU system and a 9 million euro budget, the network reaches 97.3 percent of residents within four minutes, 2.2 minutes on average. Three quarters lie within reach of two stations, and no two stations are closer than 1 km. Most sites are volunteer fire brigades: they are spread evenly across the city, which is exactly why they work. Switch to the live demo in the planner here.

### Slide 8 · `resilience`

Resilience & scenarios

## Worst station failure: −4.6%, re-planned to 97%

**Change the target time**

| Target | Sites | Coverage |
|---|---|---|
| 3 min | 31 | 84.9% |
| 4 min | 27 | 97.3% |
| 5 min | 22 | 99.1% |
| 6 min | 18 | 99.8% |

**Change the budget**

| Budget | Sites | Coverage |
|---|---|---|
| €4M | 6 | 57.5% |
| €6M | 19 | 95.1% |
| €9M | 27 | 97.3% |
| €12M | 27 | 97.3% |

The most critical site is fire station 6 (Scharnhorst): its failure costs 4.6%; re-planning around it restores 97.1%. Every variant can be saved, copied and compared as a scenario in the planner.

Above about €7M the budget no longer binds: further sites would each add less than 0.4% coverage.

> **Speaker notes:** This is the bonus in the brief. Budget, mission count, target time and failures are sliders, and each variant can be stored as a named scenario, copied and compared side by side. For discussion: below 6 million coverage drops fast, above about 7 million more money adds almost nothing. The target time is the strongest lever: going from 4 to 5 minutes saves five sites.

### Slide 9 · `operations`

Control centre & maintenance

## From emergency call to live video in 2.2 minutes

**Control centre**

- Alert from the agency dispatch via interface

- Automatic assignment to the fastest free station

- Remote pilot takes over, live video to requester

- 2 seats 24/7 = 11 full-time staff

**Maintenance**

- Two hubs: fire station 2 (north) and 4 (south)

- One spare drone and parts per hub

- Remote diagnostics, batteries swapped by cycles

- On-site swap in under 60 minutes

**Redundancy**

- Busy station: overflow to the neighbour

- Station failure: 75% of the area doubly covered

- Vehicle teams with hand-held drones as fallback

- Link loss: return home or emergency landing site

> **Speaker notes:** The control-centre flow: the fire or police dispatch raises an alert, our system picks the fastest free station, the drone launches automatically and a remote pilot supervises the flight. The live video goes straight to the requesting unit. Maintenance is centralised at two fire stations so every site is reachable within an hour.

### Slide 10 · `law`

Law & airspace

## The agencies keep authority, Morpheus flies

| Topic | Risk | Measure | Level |
|---|---|---|---|
| Sovereign powers | No official acts by private firms | Morpheus only a technical provider | Medium |
| § 21k LuftVO | Agency exemption not transferable | Specific category: SORA + LBA | High |
| BVLOS | SAIL II–III over housing | Parachute, geofencing, DAA | High |
| Dortmund airport | CTR, 2 sites in the vicinity | Coordination with DFS and airport | Medium |
| UAS geozones | Hospitals, nature, industry | Consent per geozone (dipul.de) | Medium |
| Data protection | Footage of bystanders | Purpose limits, deletion, EU hosting | Medium |

Tasking, mission decisions and data stay with the requesting agency. Morpheus provides aircraft, remote pilots and the control centre.

No blanket exemption assumed: relief is checked per mission type. Have the legal assessment confirmed by specialist lawyers.

> **Speaker notes:** The core point: Morpheus takes on no sovereign tasks, it provides aircraft and pilots. The requesting agency decides on the mission and owns the data. The biggest risk is how the operation is classified: we plan conservatively with the specific category, SORA and an operating authorisation instead of relying on the agency exemption.

---

## Part: 4 USP

### Slide 11 · `usp`

What makes it different

## Four minutes to anywhere in Dortmund

**Existing sites**

All 27 stations sit on fire and police property: power, access control and staff already there.

**Live re-planning**

Open data in, network out. Budget, failures and scenarios re-plan in milliseconds.

**EU, with a price tag**

Tender-compliant hardware, and we show what sovereignty costs: €2.48 per resident per year.

**One network for all**

Police, fire brigade, THW and city share one fleet, one control centre and one priority rule.

In one sentence: the emergency-services drone network Dortmund doesn’t have yet, planned from open data and ready to re-plan when anything changes.

> **Speaker notes:** Our USP in four parts. We don’t need new real estate: every station is on property the agencies already own. The plan is not a one-off study but a live model. We meet the European tender rule and can say exactly what it costs. And it is one network for everyone instead of four separate fleets.

---

## Part: 5 Team

### Slide 12 · `team`

Team

## Team Pilots: data, operations, delivery

**[Name]**

Data & optimization

[Relevant experience, one line]

**[Name]**

Product & demo

[Relevant experience, one line]

**[Name]**

Operations & law

[Relevant experience, one line]

**[Name]**

Business & pitch

[Relevant experience, one line]

**Built in 24 hours**

Open-data pipeline, optimizer, live planner in German and English, scenario management, this deck.

**What connects us**

[Why this problem matters to us, one sentence]

> **Speaker notes:** Introduce each person in one sentence: name, role, one relevant achievement. The jury weighs the team more than the idea, so be concrete. Then the proof point: everything shown today was built during the hackathon.

---

## Part: 6 Customer interest

### Slide 13 · `missions`

Mission profiles

## One shared fleet covers three in four missions

| Mission | Users | Prio | Platform |
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

Priority: P1 life · P2 situation and safety · P3 documentation. In a conflict the Morpheus control centre decides by this rule.

> **Speaker notes:** Nine mission types from the brief. The dock network handles first response for fire, search, traffic, events and crisis situations, together about three quarters of expected missions. Hazmat, indoor and wide-area mapping need special equipment. The priority rule settles conflicts when several agencies request the same drone.

### Slide 14 · `customers`

Customer interest

## Four customers, one shared need: eyes on scene first

| Customer | Their problem today | What Air Shield gives them |
|---|---|---|
| Fire brigade | Crews arrive without a view from above | Thermal live image before the first engine |
| Police | Searches and incidents need fast overview | Drone on scene in 2.2 min on average |
| THW / civil protection | Floods and damage need large-area maps | VTOL mapping on request |
| City crisis unit | No shared picture across agencies | One control centre, one live view |

Validation status: not yet tested with these customers. Next step: interviews with Feuerwehr Dortmund, Polizeipräsidium Dortmund and THW, then a three-station pilot.

> **Speaker notes:** We are honest here: we have not interviewed the agencies yet. What we have is the need from the brief and a model they can test with their own numbers. Our first step after the hackathon is talking to them.

---

## Part: 7 Market

### Slide 15 · `market`

Market & systems

## Drone-in-a-box: three European systems compared

| Dock system | Origin | Radius | Flight | Price* | Status |
|---|---|---|---|---|---|
| Nokia Drone Networks | FI | 5 km | 35 min | €150k | EU · selected |
| Azur Drones Skeyetech | FR | 4 km | 25 min | €160k | EU |
| Avy Aera + Dock (VTOL) | NL | 15 km | 70 min | €140k | EU · long range |
| Skydio X10 + Dock | US | 6 km | 40 min | €90k | Benchmark |
| Percepto Air Max | IL | 5 km | 40 min | €140k | Benchmark |
| DJI Dock 3 + M4TD | CN | 8 km | 54 min | €32k | Benchmark |

Plus European special drones: Quantum-Systems Vector (DE) for wide areas, Parrot ANAFI USA (FR) for vehicle teams, Flyability Elios 3 (CH) for indoor and hazmat.

* Estimates from manufacturer data and market research, dock incl. drone. Verify before any tender.

> **Speaker notes:** The brief only allows manufacturers from the EU, EEA or Switzerland, for both drone and dock. The three European dock systems cover this. The US, Israeli and Chinese systems appear only as a benchmark, to show what the European requirement costs. The planner’s auto mode only picks hover-capable multicopters, because first response needs minutes hovering over the scene.

---

## Part: 8 Competition

### Slide 16 · `competition`

Competition

## The alternatives today

| Alternative | Strength | Weakness |
|---|---|---|
| Each agency’s own drones | Under their own control | Duplicate cost, no shared view, pilot must drive out |
| Police helicopter | Large area, long endurance | Expensive per flight hour, not for every alert |
| Vehicle teams with hand drones | Flexible, cheap hardware | Drive time before the first image |
| Docks with non-EU hardware | Cheaper: €10.6M vs €18.2M TCO | Not allowed under the tender, data sovereignty |
| Air Shield | Automatic, 2.2 min, shared, EU | Needs BVLOS permits and a joint contract |

Qualitative comparison; drive and flight-hour costs not quantified here.

> **Speaker notes:** Our competition is not another start-up but the status quo: every agency doing its own thing. The cheaper non-EU dock option exists, and we show its numbers openly, but it fails the tender. Our own weakness is permits and getting four agencies into one contract, which is why we start with a pilot.

### Slide 17 · `sovereignty`

The cost of sovereignty

+€7.6M

is what the EU network costs over five years compared with a mixed one. That is €2.48 per resident per year for data sovereignty and a secure supply chain.

€18.2M · 97.3%

EU only (Nokia, FI): 5-year TCO · coverage

€10.6M · 97.5%

Mixed (DJI, CN): 5-year TCO · coverage

> **Speaker notes:** Both scenarios run through the same optimizer with the same parameters. The mixed network would be cheaper with about the same coverage, but it is not allowed under the tender rules. Our message: the European requirement costs about two and a half euros per resident per year.

---

## Part: 9–10 Business model and funding

### Slide 18 · `costs`

Costs & funding

## €455 per mission, shared by four partners

| Investment | € |
|---|---|
| 34 docks incl. drone | 5.10M |
| Prepare 27 sites | 0.81M |
| Special drones | 0.61M |
| Control centre, DFS coordination | 0.53M |
| Total | 7.05M |

Operations €2.23M a year · 5-year TCO €18.2M

| Partner | Share | € a year |
|---|---|---|
| Dortmund Fire Brigade | 42% | 1.53M |
| NRW Police | 36% | 1.31M |
| City (crisis unit) | 12% | 0.44M |
| THW / civil protection | 10% | 0.36M |
| Total | 100% | 3.64M |

60% base fee for availability, 40% per mission

Assumptions: 8,000 missions a year, investment spread over 5 years, estimated prices; partner shares from the assumed mission mix.

> **Speaker notes:** Annual cost is 3.64 million euros: investment spread over five years plus operations. At 8,000 missions that is 455 euros per mission, far less than a helicopter sortie. Morpheus pre-finances and operates; the partners pay a base fee for availability and a price per mission.

---

## Part: 11 Call to action

### Slide 19 · `roadmap`

Roadmap

## Three steps to a city-wide network

2027 H1

**Pilot**

3 stations in the city centre, SORA and operating permit, dispatch link

2027 H2

**Scale-up**

12 stations, routine BVLOS, maintenance hub north

2028

**City-wide**

27 stations, 97% within 4 minutes, second hub south

from 2029

**Region**

Same model for neighbouring Ruhr cities

**What we need next**

Anonymised dispatch history to calibrate demand, and the Dortmund Fire Brigade as pilot partner.

> **Speaker notes:** We start small with three stations in the city centre, where mission density is highest, and secure the permits there. The planner models every stage. Our ask: real mission data, so the model runs on actual alerts rather than residents.
