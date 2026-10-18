# Morpheus Air Shield — challenges, impact, solution, and the presentation prompt

Company: **Morpheus Logistik GmbH**, Dortmund — manufacturer-independent drone-as-a-service operator with a central control centre, BVLOS experience (SAIL II/III) and end-to-end operations (planning, permits, infrastructure, maintenance, flight ops).
Team: **Pilots**.

---

## Part 1 — The 7 challenge topics in 4 buckets

| Bucket | Challenge topics from the brief | The question it answers |
|---|---|---|
| **A. What to fly** | 01 Mission profiles & shared fleet · 02 European market & system research | Which missions, which drones, which suppliers? |
| **B. Where to fly** | 03 Fleet & site planning · 04 Open data & site optimization (+ Bonus: dynamic model) | How many stations, where, and what if things change? |
| **C. May we fly** | 05 Law, airspace & responsibility · 06 Ground risk, environment & safety | Is it legal, safe and acceptable for the city? |
| **D. Can we run it** | 07 Control centre, maintenance & economic operation | Can Morpheus operate it reliably and profitably? |

---

## Part 2 — How these challenges affect Morpheus today (our assessment)

| Bucket | Financial | Social | Environmental | Regulatory & operational |
|---|---|---|---|---|
| **A. What to fly** | Wrong platform choice = stranded hardware; EU-only rule raises capex | Agencies only trust a fleet that fits their missions | Wrong drone class = more flights, more energy | Non-EU hardware can disqualify Morpheus from public tenders |
| **B. Where to fly** | Too many stations burn capital, too few lose the contract | Uncovered districts = unequal emergency response | Badly placed stations = longer flights, more noise | Without a defensible siting model, no basis for permits or funding |
| **C. May we fly** | Permits, insurance and liability cost money and time | Privacy and noise concerns can block public acceptance | Nature reserves, noise and emergency landing areas must be respected | §21k LuftVO, SORA, airport control zone, sovereign powers: highest business risk |
| **D. Can we run it** | Unclear cost per mission = no price model for four agencies | 24/7 availability is a promise to citizens | Battery logistics and maintenance trips add footprint | Station failures, peaks and staffing must be planned, not improvised |

---

## Part 3 — How our prototype tackles each bucket

| Bucket | Our solution (Air Shield Planner) | Proof |
|---|---|---|
| **A. What to fly** | Mission catalogue with priority P1–P3; shared dock fleet for first response, special drones for the rest; EU/EEA/CH system comparison; non-EU only as benchmark | 9 mission types; optimizer picks the best EU dock system (Nokia Drone Networks, FI) |
| **B. Where to fly** | Optimizer on Dortmund open data: honeycomb of 769 hexagons, 612,065 residents, 48 existing fire and police sites; stations ≥1 km apart; live re-planning and saved scenarios | 27 stations · 97.3% of residents within 4 min · 2.2 min average · re-plans in ~50 ms |
| **C. May we fly** | Morpheus as technical provider, agencies keep sovereign powers and data; specific category with SORA, no blanket exemption; airport sites flagged for DFS; hospitals and geozones in the model | Worst station failure −4.6%, re-planned back to 97.1%; airport sites can be switched off (94.4%) |
| **D. Can we run it** | Fleet sized for peak load (Erlang-B); 24/7 remote pilots; two maintenance hubs; full cost model and cost split | €7.05M investment · €2.23M/yr · €455 per mission · split fire 42% / police 36% / city 12% / THW 10% |

Cost of the EU rule (tender requirement): **+€7.6M over five years = €2.48 per resident per year** compared with the cheapest non-EU docks.

---

## Part 4 — Prompt for the presentation tool

Copy everything between the lines into the PowerPoint/AI presentation tool.

=== PROMPT START ===

Create a 16-slide pitch presentation in English for a hackathon jury.
Company we built it for: Morpheus Logistik GmbH (Dortmund). Our team: Pilots. Product: “Air Shield”, a city-wide drone network for emergency services in Dortmund, planned with our live optimizer prototype.
Keep every number exactly as written; do not invent statistics, customers or quotes. One message per slide; the slide title is the message. Light humour only on the intro and closing slides.

Slide 1 — Introduction
Title: Team Pilots presents: Dortmund Air Shield
Subtitle: The emergency-services drone network Dortmund doesn’t have yet — 4 minutes to anywhere.
Our taglines (show 2–3 of them, playful):
- “In drones we trust.”
- “Nokia started with rubber boots. We started with drones.” (Nokia Drone Networks is the system our optimizer chose.)
- “Some build rockets for Mars. We build a network for Dortmund.”
- “The next big thing in Dortmund isn’t on the pitch. It’s above it.”
- “Pilots — we take the pilot out of the car and put the drone in the air.”
Footer: Morpheus Logistik · DO-Data-Hackathon 2026 · Challenge 01

Slide 2 — Who we built this for: Morpheus Logistik
Dortmund-based, manufacturer-independent drone-as-a-service operator. Builds scalable route networks instead of one-off solutions, runs a central control centre in Dortmund, has BVLOS experience (SAIL II/III), and covers planning, permits, infrastructure, maintenance and operations end to end. Fields: medical and industrial logistics, security and critical infrastructure.

Slide 3 — The challenge: 7 topics, 4 questions
A. What to fly — mission profiles, European drone market
B. Where to fly — fleet and site planning, open data and optimization
C. May we fly — law, airspace, ground risk, environment
D. Can we run it — control centre, maintenance, economics
Show as four boxes with the original topic numbers (01–07) inside.

Slide 4 — How the challenges hit Morpheus today
A 4×4 matrix: rows A–D, columns Financial · Social · Environmental · Regulatory & operational.
A: stranded hardware, EU rule raises capex · agencies need a fleet that fits · wrong drone class means more flights · non-EU hardware can disqualify tenders
B: too many stations burn capital, too few lose the contract · uncovered districts mean unequal response · bad siting means longer flights and more noise · no defensible siting, no permits or funding
C: permits, insurance, liability cost time and money · privacy and noise concerns · nature reserves, noise, landing areas · §21k LuftVO, SORA, airport control zone, sovereign powers
D: no clear cost per mission, no price model · 24/7 availability is a promise to citizens · battery and maintenance trips · failures and peaks must be planned

Slide 5 — Our answer: Air Shield
27 docked drone stations on existing fire and police sites, one Morpheus control centre, shared by fire brigade, police, THW and the city. Priority rule: P1 life, P2 situation and safety, P3 documentation. The agencies decide and own the data; Morpheus flies.

Slide 6 — A. What to fly
9 mission types (fire, missing persons, hazmat, collapse, traffic, major events, floods, damage mapping, crisis management). Shared dock fleet for first response; special drones for hazmat, indoor and wide-area mapping. EU/EEA/CH systems compared: Nokia Drone Networks (FI), Azur Drones Skeyetech (FR), Avy Aera VTOL (NL). Non-EU systems only as benchmark. Optimizer’s choice: Nokia Drone Networks.

Slide 7 — B. Where to fly
Built on Dortmund open data: 612,065 residents, 62 districts, 48 fire and police sites, 18 hospitals. The city is split into a honeycomb of 769 hexagons (0.36 km² each). The optimizer places stations at least 1 km apart, values backup coverage, and re-plans in about 50 ms.
Result: 27 stations · 97.3% of residents within 4 minutes · 2.2 min average · 74.7% covered by two stations.

Slide 8 — C. May we fly
Morpheus is the technical provider; sovereign powers and data stay with the agencies. Operation in the specific category with SORA and LBA approval — no blanket §21k LuftVO exemption assumed. BVLOS with parachute, geofencing, detect-and-avoid. Two airport-area sites need DFS coordination (without them: 94.4%). Hospitals and geozones are in the model. Data protection: purpose limits, deletion periods, EU hosting.

Slide 9 — D. Can we run it
Alert → automatic assignment to the fastest free station → remote pilot → live video to the agency. 2 control seats 24/7 (11 staff), two maintenance hubs, drone swap under 60 minutes. Fleet sized for peak load. Worst single station failure: −4.6%, re-planning restores 97.1%.

Slide 10 — The engine: an optimizer with scenario planning
Explain simply, as a flow from left to right:
- What is an optimizer? A tool that searches thousands of possible plans and returns the best one for a goal, within given limits.
- Goal: reach as many residents as possible within the target time, with backup coverage where possible.
- Decisions: which of the 48 fire and police sites get a station, which drone system, how many docks per site.
- Parameters (what you set): budget, target response time, missions per year, dock system.
- Restrictions (what must hold): stay within budget, stations at least 1 km apart, drone range, airport zone rules, EU-only hardware.
- Output: the best plan — stations, docks, coverage, response time, costs — in about 50 milliseconds.
Scenario planning: every set of parameters can be saved as a scenario, copied and compared side by side. A station failure can be simulated with one click and the network re-plans itself.

Slide 11 — Why we recommend this scenario
Recommended scenario: 4-minute target, €9M budget, EU hardware → 27 stations, 97.3% of residents, €7.05M investment.
Why (keep it short, four reasons):
- Sweet spot of speed: 3 minutes is physically limited (only 85% even with more stations); 5 minutes is cheaper but slower for every emergency.
- Diminishing returns: above about €7M each extra station adds less than 0.4% coverage — so we stop at €7.05M and keep headroom.
- Robust: 75% of the city is covered by two stations; losing the most important one costs 4.6% and re-planning restores 97%.
- Tender-compliant: EU hardware only, with the cost of that choice made transparent.
Small footnote: other scenarios (Pilot €2.5M, Phase 1 €4M, Lean €6M) are the rollout steps toward it.

Slide 12 — Business model and the cost of sovereignty
Investment €7.05M · operations €2.23M a year · 5-year total €18.2M · €455 per mission at 8,000 missions a year.
Drone-as-a-service: Morpheus pre-finances and operates; partners pay 60% availability fee and 40% per mission. Annual cost split: fire brigade 42%, police 36%, city 12%, THW 10%.
EU-only costs +€7.6M over five years versus the cheapest non-EU docks = €2.48 per resident per year for data sovereignty and a secure supply chain.

Slide 13 — Roadmap and our ask
2027 H1 pilot with 3 stations · 2027 H2 12 stations, routine BVLOS · 2028 all 27 stations · from 2029 the Ruhr region, and medical deliveries between Dortmund’s 18 hospitals with the same engine.
Our ask: anonymised dispatch data and Feuerwehr Dortmund as pilot partner.

Slide 14 — Team Pilots
Four people, each with photo, name, role, one line of relevant experience and a QR code to their LinkedIn profile:
- [Name] — Data & optimization — [one line] — QR: [LinkedIn URL]
- [Name] — Product & demo — [one line] — QR: [LinkedIn URL]
- [Name] — Operations & law — [one line] — QR: [LinkedIn URL]
- [Name] — Business & pitch — [one line] — QR: [LinkedIn URL]
Line at the bottom: “Built in 24 hours: open-data pipeline, optimizer, live planner, scenarios, this deck.”

Slide 15 — Live demo (60 seconds)
Title: Let’s fly it — live.
Three steps shown as a small checklist:
1. The map: honeycomb = coverage, circles = each station’s reach.
2. A station fails → −4.6% → one click re-plans back to 97%.
3. Switch scenario: Pilot → Lean → Recommended.
Note on slide: “The demo is short on purpose. Questions on details, data or the model? Come to our table — we’ll show you everything.”

Slide 16 — Closing
Title: Four minutes to anywhere in Dortmund.
Subtitle: In drones we trust. Thank you!
Team Pilots · contact: [email] · LinkedIn QR codes on the previous slide.

=== PROMPT END ===
