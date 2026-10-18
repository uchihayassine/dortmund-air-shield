# Dortmund Air Shield — project notes

Team **Pilots** · DO-Data-Hackathon 2026 (Dortmund, 16–17 Oct 2026) · Challenge 01 by **Morpheus Logistik GmbH**

Status of this file: 17 Oct 2026. All figures refer to the **★ Recommended** scenario unless stated otherwise.

---

## 1. Links and files

| What                                             | Where                                                                                                                                                  |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Live planner (prototype)                         | https://claude.ai/artifact/8cDW4CvauKbHW9xBXpFVLK                                                                                                      |
| Pitch deck (19 slides, English)                  | https://claude.ai/artifact/FJ9M2YcumqxRwVyPRG1sF1                                                                                                      |
| Challenge briefing                               | `Morpheus_DO_DATA_Hackathon_2026_Challenges-1.pdf`                                                                                                     |
| Planner source                                   | `app/planner.template.html` → build → `app/air-shield-planner-en.html`                                                                                 |
| Build scripts                                    | `tools/build_data.py`, `tools/build_basemap.py`, `tools/build_app.py`                                                                                  |
| Data                                             | `data/raw/` (open-data downloads), `data/airshield_data.json`, `data/basemap/`                                                                         |
| Calculation methods (formulas + worked examples) | `CALCULATION_METHODS.md`                                                                                                                               |
| All data, assumptions and results as CSV         | `data/export/*.csv` (24 files, regenerate with `node tools/export_csv.js` and `python tools/export_raw_csv.py`; list in `CALCULATION_METHODS.md`)      |
| Artifacts, local exports, how to export PPTX/PDF | `ARTIFACTS.md` · deck source `presentation/deck_EN/` · deck text `presentation/deck_EN.md`                                                             |
| Presentation material                            | `presentation/` — `pitch_prompt_morpheus.md` (16-slide prompt), `gamma_air_shield_EN.md`, `gamma_prompt_EN.md`, `pitch_plan.md`, `planner_guide_EN.md` |

Both links are private until shared via the page’s Share menu.

---

## 2. Company

**Morpheus Logistik GmbH**, Dortmund (from the briefing): manufacturer-independent drone-as-a-service operator. Builds scalable route networks instead of isolated solutions, runs a central control centre in Dortmund, has BVLOS experience (SAIL II/III), covers planning, permits, infrastructure, maintenance and operations end to end. Fields: medical and industrial logistics, security, critical infrastructure.

---

## 3. Problem

### 3.1 The brief

Plan a city-wide, manufacturer-independent drone network for police, fire brigade, THW and other public safety agencies (BOS) in Dortmund, operated centrally by Morpheus: missions, European drones and docks, fleet size, sites, maintenance, law, costs. Bonus: an optimization model that re-plans when budget, mission numbers or station failures change.

### 3.2 Seven topics → four buckets

| Bucket           | Topics in the brief                                                       | Question                                         |
|------------------|---------------------------------------------------------------------------|--------------------------------------------------|
| A. What to fly   | 01 Mission profiles & shared fleet · 02 European market & system research | Which missions, drones, suppliers?               |
| B. Where to fly  | 03 Fleet & site planning · 04 Open data & site optimization (+ bonus)     | How many stations, where, what if things change? |
| C. May we fly    | 05 Law, airspace & responsibility · 06 Ground risk, environment & safety  | Legal, safe, acceptable?                         |
| D. Can we run it | 07 Control centre, maintenance & economics                                | Reliable and profitable operation?               |

### 3.3 Impact on Morpheus (our assessment, not company statements)

| Bucket | Financial                                                 | Social                                               | Environmental                            | Regulatory & operational                                  |
|--------|-----------------------------------------------------------|------------------------------------------------------|------------------------------------------|-----------------------------------------------------------|
| A      | Wrong platform = stranded hardware; EU-only raises capex  | Agencies only trust a fleet that fits their missions | Wrong drone class = more flights, energy | Non-EU hardware can disqualify tenders                    |
| B      | Too many stations burn capital, too few lose the contract | Uncovered districts = unequal emergency response     | Bad siting = longer flights, more noise  | No defensible siting model = no permits or funding        |
| C      | Permits, insurance, liability cost time and money         | Privacy and noise can block acceptance               | Nature reserves, noise, landing areas    | §21k LuftVO, SORA, airport control zone, sovereign powers |
| D      | No clear cost per mission = no price model                | 24/7 availability is a promise to citizens           | Battery and maintenance trips            | Failures and peaks must be planned                        |

---

## 4. Solution

**Air Shield**: 27 docked drone stations on existing fire and police sites, one Morpheus control centre, shared by fire brigade, police, THW and city. Priority rule: P1 life · P2 situation & safety · P3 documentation. Agencies decide on missions and own the data; Morpheus is the technical operator.

| Bucket | How the prototype answers it                                                                                                                             |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| A      | Mission catalogue (9 types, P1–P3); shared dock fleet + special drones; EU/EEA/CH systems compared, non-EU only as benchmark; optimizer picks the system |
| B      | Optimizer on open data: 769 hexagons, 48 candidate sites, ≥1 km spacing, backup coverage; live re-planning, failure simulation, saved scenarios          |
| C      | Operating model (agencies keep sovereign powers), specific category with SORA, airport sites flagged for DFS, hospitals and geozones marked              |
| D      | Docks sized for peak load (Erlang-B), 24/7 remote pilots, two maintenance hubs, full cost model and cost split                                           |

### Missions (9)

Fire/smoke (P1), missing-person search (P1), hazmat/CBRN (P1), collapse/indoor (P1), traffic accident (P2), major event (P2), flood/heavy rain (P2), damage mapping (P3), municipal crisis management (P3).

### Legal approach (needs confirmation by lawyers)

- Morpheus provides aircraft, pilots and control centre; no sovereign acts.
- Operation in the specific category with SORA and LBA approval; no blanket §21k LuftVO exemption assumed.
- BVLOS with parachute, geofencing, detect-and-avoid; SAIL II–III.
- Dortmund airport: 2 sites in the vicinity need DFS/airport coordination.
- Data protection: purpose limitation, deletion periods, EU hosting.

---

## 5. Prototype — the Air Shield Planner

Single web page (HTML + JavaScript + D3.js), all calculations in the browser, no server.

### 5.1 Inputs (drivers) vs outputs

| Inputs (left panel + hidden assumptions)                                                                                                                                                                                                        | Outputs (right panel + sections below)                                                                                                                                                                              |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Suppliers (EU only / mixed), capital budget, target response time, missions per year, dock system, backup weight β, minimum gain per station, peak factor, max. overflow, minimum station spacing, airport sites on/off, failed/banned stations | Chosen system, sites, docks, coverage, redundancy, average response time, investment, operations per year, 5-year TCO, cost per mission, worst single failure, cost of sovereignty, cost split, scenario comparison |

### 5.2 How it calculates (full formulas and worked examples: `CALCULATION_METHODS.md`)

 1. **Demand:** 769 pointy-top hexagons (0.36 km² each = area of a 600 m square); district population spread evenly over its hexagons; extra weight at 8 hotspots.
 2. **Distances:** haversine distance from every hexagon to every candidate (769 × 48 matrix).
 3. **Coverage:** hexagon covered by a station if launch time + distance × 1.15 ÷ speed ≤ target time **and** distance ≤ drone range. Reach radius = min(range, (target − launch) × speed ÷ 1.15).
 4. **Objective:** maximize Σ weight × (1 for first covering station + β for second).
 5. **Greedy:** repeatedly add the site with the highest gain per euro that fits the budget, adds ≥ minimum gain, and is ≥ minimum spacing from all chosen sites.
 6. **Swap improvement:** replace each chosen site with each unused one if it improves the objective (incremental delta, up to 3 passes).
 7. **Fleet sizing:** missions assigned to the fastest station; peak-hour load a = missions ÷ 8,760 × peak factor × service time (flight there and back + 15 min on scene + recharge); Erlang-B, docks = smallest c with blocking ≤ max overflow.
 8. **Budget fit:** if docks push total investment over budget, the site budget shrinks and the plan is recomputed (max. 8 times); last resort drops the least-used site.
 9. **Automatic system choice:** steps 3–8 for each eligible hover-capable dock system; best coverage wins, cheaper one if within 0.5 %.
10. **Robustness:** each station switched off in turn; largest coverage loss reported.
11. **Cost of sovereignty:** full optimization for EU-only and for mixed with identical settings; difference in 5-year TCO ÷ residents ÷ 5.

Runtime ~30–50 ms per full run. Results cached per parameter set. Scenarios saved in the browser’s localStorage (per viewer, not shared).

### 5.3 Cost formulas

- **Investment** = docks × dock price + sites × €30k + airport sites × €40k + special drones €0.61M + control-centre integration €0.45M
- **Operations / year** = docks × (system opex + €4.5k insurance) + seats × 5.5 FTE × €82k + software €0.22M + 12 % of special-drone value
- **Seats** = max(2, ⌈peak simultaneous flights ÷ 3⌉)
- **5-year TCO** = investment + 5 × operations
- **Cost per mission** = (investment ÷ 5 + operations) ÷ missions per year
- **Cost split** = annual cost × agency share

---

## 6. Assumptions and data sources

Legend: **Sourced** = from a named public source · **Estimate** = our estimate, not verified · **Choice** = deliberate modelling decision.

### 6.1 Data

| Item                       | Value                                                                                                                  | Status   | Source                                                          |
|----------------------------|------------------------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------|
| District boundaries        | 62 statistical districts                                                                                               | Sourced  | open-data.dortmund.de, dataset `fb62-statistischebezirke`       |
| Population 2023            | 612,065                                                                                                                | Sourced  | `ds-bevolkerung-nach-geschlecht-und-migrationshintergrund-2023` |
| Fire brigade sites         | 32 (deduplicated with police → 48 candidates)                                                                          | Sourced  | dataset `feuerwehr`                                             |
| Police sites               | 21 (Lünen-Brambauer and water police excluded)                                                                         | Sourced  | dataset `polizei`                                               |
| Hospitals                  | 18 (KrankenhausKlinik only)                                                                                            | Sourced  | dataset `krankenhaus`                                           |
| Street map                 | Dortmund, zoom 13                                                                                                      | Sourced  | © OpenStreetMap contributors (tiles downloaded once)            |
| Hotspots                   | Stadium +20k, Hbf +12k, Westfalenhallen +8k, Hafen +6k, airport +6k, Phoenix-See +5k, TU +5k, Westfalenpark +4k weight | Estimate | Coordinates approximate                                         |
| Airport                    | DTM at 51.5183 N, 7.6122 E; near zone 2.5 km, CTR 6 km                                                                 | Estimate | Schematic — check geozones on dipul.de                          |
| Population within district | Evenly spread                                                                                                          | Choice   | —                                                               |

### 6.2 Recommended scenario inputs

| Input                    | Value                            | Status                                  |
|--------------------------|----------------------------------|-----------------------------------------|
| Suppliers                | EU / EEA / CH only               | Brief requirement                       |
| Capital budget           | €9.0M                            | Choice                                  |
| Target response time     | 4 min                            | Choice                                  |
| Missions per year        | 8,000 (~22 per day)              | Estimate — not from dispatch statistics |
| Dock system              | Automatic → Nokia Drone Networks | Output of optimizer                     |
| Backup weight β          | 0.5                              | Choice                                  |
| Minimum gain per station | 0.4 %                            | Choice                                  |
| Peak factor              | ×3                               | Estimate                                |
| Max. overflow at peak    | 10 %                             | Choice                                  |
| Minimum station spacing  | 1 km                             | Choice                                  |
| Airport sites            | Allowed with DFS coordination    | Choice                                  |

### 6.3 Drone systems (all Estimate — verify with vendors)

| System                   | Origin | Type                         | Speed  | Range | Launch | Flight | Recharge | Dock incl. drone | Opex/yr |
|--------------------------|--------|------------------------------|--------|-------|--------|--------|----------|------------------|---------|
| Azur Drones Skeyetech    | FR     | Multicopter dock             | 15 m/s | 4 km  | 30 s   | 25 min | 30 min   | €160k            | €28k    |
| Nokia Drone Networks     | FI     | Multicopter dock             | 16 m/s | 5 km  | 45 s   | 35 min | 35 min   | €150k            | €26k    |
| Avy Aera + Dock          | NL     | VTOL dock (manual only)      | 25 m/s | 15 km | 90 s   | 70 min | 40 min   | €140k            | €25k    |
| DJI Dock 3 + Matrice 4TD | CN     | Multicopter dock (benchmark) | 15 m/s | 8 km  | 25 s   | 54 min | 32 min   | €32k             | €9k     |
| Skydio X10 + Dock        | US     | Multicopter dock (benchmark) | 16 m/s | 6 km  | 25 s   | 40 min | 30 min   | €90k             | €15k    |
| Percepto Air Max         | IL     | Multicopter dock (benchmark) | 14 m/s | 5 km  | 40 s   | 40 min | 30 min   | €140k            | €24k    |

Special drones (EU): 2 × Quantum-Systems Vector (€180k), 8 × Parrot ANAFI USA GOV (€14k), 1 × Flyability Elios 3 (€140k) = €0.61M. Mixed: DJI Matrice 350 + H30T, DJI Mavic 3T, Elios 3.

### 6.4 Cost and operating parameters (all Estimate)

| Parameter                                | Value                                                                                           |
|------------------------------------------|-------------------------------------------------------------------------------------------------|
| Detour factor                            | 1.15 × straight line                                                                            |
| Time on scene                            | 15 min                                                                                          |
| Site preparation (power, network, fence) | €30k per site                                                                                   |
| Airport coordination                     | €40k per airport-area site                                                                      |
| Control-centre integration               | €450k one-off                                                                                   |
| Software / UTM / data                    | €220k per year                                                                                  |
| Remote pilot                             | €82k per FTE per year; 1 pilot supervises up to 3 flights; 24/7 seat = 5.5 FTE; minimum 2 seats |
| Insurance                                | €4.5k per dock per year                                                                         |
| Special drones upkeep                    | 12 % of value per year                                                                          |
| Depreciation period                      | 5 years                                                                                         |
| Cost split                               | Fire brigade 42 %, police 36 %, city 12 %, THW 10 %                                             |
| Fee model                                | 60 % availability fee, 40 % per mission                                                         |

---

## 7. Results

### 7.1 Recommended scenario (★ 4 min · €9M · 8,000 missions · EU only)

| Output                  | Value                                                                                   |
|-------------------------|-----------------------------------------------------------------------------------------|
| System                  | Nokia Drone Networks (FI), reach 2.7 km                                                 |
| Stations · docks        | 27 · 34 (12 volunteer fire brigades, 5 fire stations, 10 police stations)               |
| Population within 4 min | 97.3 %                                                                                  |
| Average response        | 2.2 min                                                                                 |
| Covered by ≥ 2 stations | 74.7 %                                                                                  |
| Investment              | €7.05M (docks €5.10M, sites €0.81M, special drones €0.61M, control centre + DFS €0.53M) |
| Operations              | €2.23M per year                                                                         |
| 5-year TCO              | €18.2M                                                                                  |
| Annual cost             | €3.64M (≈ €5.95 per resident)                                                           |
| Cost per mission        | €455                                                                                    |
| Remote pilots           | 2 seats 24/7 = 11 FTE (€0.90M/yr)                                                       |
| Worst single failure    | Feuer- und Rettungswache 6 Scharnhorst: −4.6 %; re-planned 97.1 %                       |
| Cost of sovereignty     | +€7.6M over 5 years vs DJI mixed (€10.6M TCO, 97.5 %) = €2.48 per resident per year     |

Budget does not bind: the optimizer stops at €7.05M because further sites add < 0.4 % each.

### 7.2 Preset scenarios

| Scenario                             | Changes vs recommended       | Result                                        |
|--------------------------------------|------------------------------|-----------------------------------------------|
| ★ Recommended: 4 min · €9M           | —                            | 27 sites · 97.3 % · €7.05M · €455/mission     |
| Pilot 2027: €2.5M                    | budget €2.5M                 | 3 sites · 36 %                                |
| Phase 1: €4M                         | budget €4M                   | 6 sites · 58 %                                |
| Lean city-wide: €6M                  | budget €6M                   | 19 sites · 95 %                               |
| Faster: 3-minute response            | target 3 min, budget €12M    | 31 sites · 85 % (reach limit)                 |
| Relaxed: 5-minute response           | target 5 min                 | 22 sites · 99 %                               |
| Major incident year: 20,000 missions | missions 20,000, budget €12M | 27 sites · 48 docks · €224/mission            |
| No sites near the airport            | airport sites off            | 26 sites · 94 %                               |
| Benchmark: mixed suppliers           | mixed                        | DJI · €2.6M investment · not tender-compliant |

### 7.3 Main drivers (sensitivity)

- **Coverage:** target time, launch time and cruise speed (they set the reach radius) dominate; budget matters only below ~€7M.
- **Cost:** dock price, peak factor and allowed overflow (docks per site), recharge time; missions per year mainly changes cost per mission.
- **Site count:** the backup weight β — without it ~19 sites give the same coverage but no redundancy.

---

## 8. Limitations (say them openly)

- Prices, specs, mission volume and cost rates are estimates.
- Population spread evenly within districts; no real alert data.
- Straight-line flight × 1.15; no weather, night or wind limits; no obstacle model.
- Airport zone schematic; real geozones not imported.
- Heuristic optimizer: very good, not proven optimal.
- Agencies not interviewed; cost split assumed.
- Legal assessment not reviewed by lawyers.

---

## 9. Open items

- Team names, roles, one-line experience, LinkedIn URLs (QR codes), contact email.
- Replace estimates with sources: Feuerwehr Dortmund annual report (missions), vendor quotes or tender results (dock prices), TVöD (pilot salary), insurer rates.
- Optional: exact MILP check (e.g. PuLP/HiGHS) to quote the heuristic’s gap.
- Optional: medical deliveries between the 18 hospitals as a second use case.

---

## 10. Rebuild

```bash
python tools/build_data.py
python tools/build_app.py
node tools/export_csv.js
python tools/export_raw_csv.py
```

`build_basemap.py` only needs to run again if the map area changes (downloads OpenStreetMap tiles).

---

## 11. Glossary

| Term                  | Meaning                                                                      |
|-----------------------|------------------------------------------------------------------------------|
| BOS                   | Behörden und Organisationen mit Sicherheitsaufgaben — public safety agencies |
| BVLOS                 | Beyond visual line of sight                                                  |
| SORA                  | Specific Operations Risk Assessment (EASA)                                   |
| SAIL                  | Specific Assurance and Integrity Level (risk class from SORA)                |
| CTR                   | Control zone around an airport                                               |
| DFS                   | German air navigation service                                                |
| LBA                   | German Federal Aviation Office                                               |
| Drone-in-a-box / dock | Weatherproof station where a drone lives, charges and launches automatically |
| Erlang-B              | Queueing formula: chance that all docks are busy at peak                     |
| TCO                   | Total cost of ownership (here 5 years)                                       |
| Target response time  | Alert → drone over the scene (launch + flight), excluding dispatch handling  |
