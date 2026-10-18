# Dortmund Air Shield — problems, prototype, pitch

## 1. Problems and how the prototype solves them

| # | Problem (from the brief and from reality) | What the prototype does | Where to show it |
|---|---|---|---|
| 1 | Every agency buys its own drones: police, fire brigade, THW, city. Duplicate cost, no shared control. | One shared dock network, run by Morpheus as a neutral operator, with a priority rule (P1 life, P2 situation, P3 documentation). | Deck: Team Pilots slides 2–3, mission profiles |
| 2 | Nobody knows where stations should go. | Optimizer on Dortmund open data: 769 hexagons, 612,065 residents, 48 existing fire and police sites. Picks 27 sites for 97.3 % coverage within 4 min. | Planner: map, "Result" panel |
| 3 | How many drones, how much money? | Docks per site sized for peak load (Erlang-B); investment, operating cost, 5-year TCO and cost per mission computed live (€7.1M, €2.23M/yr, €455 per mission). | Planner: "Fleet & costs" |
| 4 | What if a station fails? | Click a station to fail it: coverage drops at most 4.6 %; "Re-plan" restores 97.1 %. Minimum 1 km between stations so backup is real. | Planner: click a station |
| 5 | Budget and politics change. | Sliders for budget, target time, missions; saved scenarios that can be copied and compared side by side. This is the brief’s bonus. | Planner: Scenario panel + comparison table |
| 6 | Tender requires EU/EEA/CH hardware, but it costs more. | Same optimizer runs EU-only vs mixed suppliers: EU costs +€7.6M over 5 years = €2.48 per resident per year. | Planner: "Cost of sovereignty" |
| 7 | Airspace and ground risk (airport, hospitals). | Airport vicinity flagged (DFS coordination), hospitals marked as sensitive, sites can be excluded. | Planner: map + alerts |
| 8 | Legal: a private firm cannot exercise sovereign powers. | Operating model: agencies decide and own the data, Morpheus flies; specific category with SORA, no blanket exemption assumed. | Deck: law slide |
| 9 | Who pays? | Cost split between four partners (60 % availability fee, 40 % per mission). | Planner + deck: costs |

**Be honest about (the pitch training says: do not fabricate):**
- Drone prices and specs are estimates; airport zone is schematic; population is spread evenly inside each district; the optimizer is a heuristic, not a proven optimum.
- Say it as strength: “every assumption is a slider — give us real dispatch data and the model recalculates.”

## 2. Our deck vs the 11-part pitch structure

| Pitch part | Our slide | Status | To do |
|---|---|---|---|
| 1. Introduction (one memorable sentence) | Cover | OK | Add the one-liner: **“The emergency-services drone network Dortmund doesn’t have yet: 4 minutes to anywhere.”** |
| 2. Problem | Team Pilots slide 2 (scattered drones) + challenge slide | OK | Keep the scattered-drones animation as the emotional hook |
| 3. Product | Slide 3 (drones organize) + model + result + live demo | Strong | Demo max. 60 s, product must not dominate |
| 4. USP | — | **Missing** | One slide: open-data optimizer + live what-if + EU-compliant + uses existing fire/police sites |
| 5. Team | Team Pilots slides | **Thin** | Names, roles, one line of relevant experience each (data, optimization, ops, law) |
| 6. Customer interest | — | **Missing** | Who needs it: fire brigade, police, THW, city. Honest: “not validated with customers yet; next step is a pilot with Feuerwehr Dortmund.” |
| 7. Market | Market slide (systems) | Partial | Add: Germany has ~80 cities > 100k inhabitants; same model scales (Ruhr region first) |
| 8. Competition | Market slide | Partial | Today’s alternative: each agency’s own drones and car-based teams (10–20 min to scene) |
| 9. Business model | Costs slide | OK | Drone-as-a-service: availability fee + per-mission price |
| 10. Funding | Costs slide | OK | €7.1M investment, €3.6M/yr all-in |
| 11. Call to action | Roadmap | OK | End on the ask: dispatch data + pilot partner, 3 stations in 2027 |

## 3. Three-minute pitch script (about 400 words)

**0:00 Hook — slide 2, scattered drones**
“Dortmund already flies drones for emergencies. But each agency has its own, from different makers, with no shared control. When a fire breaks out in Scharnhorst, nobody knows which drone is closest.”

**0:20 Solution — press next, drones organize**
“We are Team Pilots. Air Shield turns this into one network: 27 docked stations on existing fire and police sites, chosen by our optimizer from Dortmund’s open data. 97 % of residents reached within four minutes, 2.2 minutes on average.”

**0:45 Live demo — planner, 60 seconds**
1. Show the map and the result panel.
2. Click Scharnhorst station → “fails” → coverage −4.6 % → Re-plan → back to 97 %.
3. Switch scenario ★ Recommended → Lean city-wide (€6M): 19 stations, 95.1 %.
“Every assumption is a slider. Budget, response time, failures — the network re-plans in milliseconds.”

**1:45 Why it’s different (USP)**
“We use buildings the city already owns, European hardware as the tender requires, and we can prove what sovereignty costs: €2.48 per resident per year.”

**2:05 Business model**
“Morpheus pre-finances and operates. Investment €7.1M, €455 per mission, shared by fire brigade, police, THW and city: a base fee for availability plus a price per mission.”

**2:30 Honest limits + ask**
“Prices are estimates and demand is based on residents, not real alarms. That’s our ask: anonymised dispatch data and the Feuerwehr Dortmund as pilot partner. Three stations in 2027, the whole city in 2028.”

**2:55 Close**
“Four minutes to anywhere in Dortmund. Thank you.”

## 4. Delivery checklist (from the training)
- One speaker per section, hand-overs rehearsed; demo person has the planner open in a second tab.
- Look at the jury, not the screen; numbers slowly: “ninety-seven percent, four minutes”.
- Prepare answers: Why not DJI? (tender + data sovereignty, cost shown) · Is it legal? (specific category, SORA, no blanket exemption) · Why trust the numbers? (open data, every assumption adjustable) · What if mobile network fails? (that’s Challenge 02; fallback: return home / landing sites).
